from audioop import reverse
from django.contrib import messages
import random
from MySQLdb import IntegrityError
from django.http import  HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django import forms
from .models import *
import uuid
from decimal import Decimal
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from django.http import JsonResponse
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect
from .forms import *
from .models import UserAccount

def fetch_user_data(request, user_id):
    if request.method == 'GET' and request.is_ajax():
        user_id = request.GET.get('user_id')
        try:
            user = Customer.objects.get(user_id=user_id) 
            user_data = {
                'email': user.email,
                'name': user.username,
                'number': user.contact_number,
                'address': user.address,
            }
            return JsonResponse({'user_data': user_data})
        except Customer.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

def generate_pdf(request, user_id):
    transactions = Transaction.objects.filter(user_id=user_id)  
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="account_statements.pdf"'
    doc = SimpleDocTemplate(response, pagesize=letter)
    data = [['Transaction ID', 'Action', 'Credit', 'Debit', 'Balance', 'Other', 'Date']]
    for transaction in transactions:
        data.append([
            transaction.transaction_id,
            transaction.action,
            transaction.credit,
            transaction.debit,
            transaction.balance,
            transaction.other,
            transaction.date.strftime('%Y-%m-%d %H:%M:%S')  
        ])
    table = Table(data)
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])
    table.setStyle(style)
    elements = []
    elements.append(table)
    doc.build(elements)
    return response


def generate_transaction_id():
    return str(uuid.uuid4())[:10]  

class UserAccountForm(forms.ModelForm):
    class Meta:
        model = UserAccount
        fields = ['user_id', 'email', 'name', 'balance', 'number', 'city', 'address', 'source', 'accountNo', 'branch', 'accountType']
        exclude = ['date']

    def clean_balance(self):
        balance = self.cleaned_data.get('balance')
        if balance < 0:
            raise forms.ValidationError('Balance must be positive.')
        return balance

    def clean_accountNo(self):
        accountNo = self.cleaned_data.get('accountNo')
        if UserAccount.objects.filter(accountNo=accountNo).exists():
            raise forms.ValidationError('Account number already exists.')
        return accountNo

def home(request):
    return render(request, "base.html")

def branch(request):
    return render(request, "branch.html", {})

def user_login(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')

        if user_type == "customer":
            try:
                user = Customer.objects.get(user_id=user_id, password=password)
                return redirect(reverse('usr_dashboard', kwargs={'user_id': user.user_id}))
            except Customer.DoesNotExist:
                return render(request, 'login.html', {'error_message': 'Invalid credentials'})
        elif user_type == "manager":
            try:
                manager = Manager.objects.get(mgr_id=user_id, password=password)
                return redirect(reverse('mgr_dashboard', kwargs={'mgr_id': manager.mgr_id}))
            except Manager.DoesNotExist:
                return render(request, 'login.html', {'error_message': 'Invalid credentials'})
        else:
            return render(request, 'login.html', {'error_message': 'Invalid user type'})

    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('login') 


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        contact_number = request.POST.get('contact_number')
        address = request.POST.get('address')
        
        while True:
            user_id = username + str(random.randint(0, 9999))
            if not Customer.objects.filter(user_id=user_id).exists():
                try:
                    Customer.objects.create(
                        user_id=user_id,
                        username=username,
                        password=password,
                        email=email,
                        contact_number=contact_number,
                        address=address
                    )
                    break
                except IntegrityError:
                    continue
        return render(request, 'registration_success.html', {'user_id': user_id})
    else:
        return render(request, 'register.html')
    
def calculate_total_balance(user_id):
    user_accounts = UserAccount.objects.filter(user_id=user_id)
    total_balance = sum(account.balance for account in user_accounts)
    return total_balance

def usr_dashboard(request, user_id):
    user = get_object_or_404(Customer, user_id=user_id)
    username = user.username
    total_balance = calculate_total_balance(user_id)    
    return render(request, 'usr_dashboard.html', {'user': username, 'total_balance':total_balance, 'user_id': user_id})

def calculate_balance():
    accounts = UserAccount.objects.filter()
    return sum(account.balance for account in accounts)

def mgr_dashboard(request, mgr_id):
    mgr = get_object_or_404(Manager, mgr_id=mgr_id)
    username = mgr.mgrname
    total_accounts = UserAccount.objects.count()
    total_transaction = Transaction.objects.count()
    total_balance = calculate_balance()
    return render(request, 'mgr_dashboard.html', {'user': username, 'total_accounts': total_accounts, 'total_transactions': total_transaction, 'total_balance': total_balance, 'account': accounts, 'mgr_id': mgr_id})

def accounts(request, mgr_id):
    accounts = UserAccount.objects.all()
    return render(request, 'accounts.html', {'accounts': accounts, 'mgr_id': mgr_id})

def account_details(request, accountNo, mgr_id):
    account = get_object_or_404(UserAccount, accountNo=accountNo)
    print(f"No {accountNo}")
    context = {
        'account':account,
        'mgr_id':mgr_id,
    }
    return render(request, 'account_details.html', context)

def add_account(request, mgr_id):
    if request.method == 'POST':
        form = UserAccountForm(request.POST)
        if form.is_valid():
            user_account = form.save(commit=False)
            user_account.save()
            return redirect('accounts', mgr_id=mgr_id)
    else:
        form = UserAccountForm()

    return render(request, 'add_accounts.html', {'form': form, 'mgr_id': mgr_id})

def usr_accounts(request, user_id):
    user_accounts = UserAccount.objects.filter(user_id=user_id)
    total_balance = calculate_total_balance(user_id)
    context = {
        'user_id': user_id,
        'user_accounts': user_accounts,
        'total_balance': total_balance,
    }
    return render(request, 'usr_accounts.html', context)

def internal_transfer(request, user_id):
    total_balance = calculate_total_balance(user_id)
    user_accounts = UserAccount.objects.filter(user_id=user_id)
    all_accounts = UserAccount.objects.exclude(user_id=user_id)
    context = {
        'user_id': user_id,
        'user_accounts': user_accounts,
        'total_balance': total_balance,
        'all_accounts': all_accounts,
    }
    return render(request, 'internal_transfer.html', context)

def external_transfer(request, user_id):
    total_balance = calculate_total_balance(user_id)
    user_accounts = UserAccount.objects.filter(user_id=user_id)
    all_accounts = UserAccount.objects.exclude(user_id=user_id)
    context = {
        'user_id': user_id,
        'user_accounts': user_accounts,
        'total_balance': total_balance,
        'all_accounts': all_accounts,
    }
    return render(request, 'external_transfer.html', context)

def account_statements(request, user_id):
    transactions = Transaction.objects.filter(user_id=user_id)
    total_balance = calculate_total_balance(user_id) 
    context = {
        'user_id': user_id,
        'transactions': transactions,
        'total_balance':total_balance,
    }
    return render(request, 'account_statements.html', context)

def self_transfer(request, user_id):
    if request.method == 'POST':
        source_account_id = request.POST.get('source_account_id')
        destination_account_id = request.POST.get('destination_account_id')

        try:
            source_account = UserAccount.objects.get(accountNo=source_account_id, user_id=user_id)
            amount = Decimal(request.POST.get('amount'))
            if source_account_id == destination_account_id:
                messages.error(request, 'Please choose different accounts!')
            else:
                destination_account = UserAccount.objects.get(accountNo=destination_account_id)
                if amount <= 0:
                    messages.error(request, 'Amount should be greater than zero!')
                elif source_account.balance >= amount:
                    source_account.balance -= amount
                    source_account.save()
                    destination_account.balance += amount
                    destination_account.save()
                    Transaction.objects.create(
                        transaction_id=generate_transaction_id(),  
                        action='transfer',
                        debit=amount,
                        credit=0,
                        balance=source_account.balance,
                        other=f'Transferred to {destination_account_id}',
                        user_id=source_account.user_id,
                        account=source_account
                    )
                    Transaction.objects.create(
                        transaction_id=generate_transaction_id(), 
                        action='transfer',
                        debit=0,
                        credit=amount,
                        balance=destination_account.balance,
                        other=f'Received from {source_account_id}',
                        user_id=destination_account.user_id,
                        account=destination_account
                    )
                    messages.success(request, 'Funds transferred successfully!')
                else:
                    messages.error(request, 'Insufficient balance!')
        except UserAccount.DoesNotExist:
            messages.error(request, 'One of the accounts does not exist!')
        except Exception as e:
            messages.error(request, str(e))

        return redirect('internal_transfer', user_id=user_id)
    else:
        return redirect('internal_transfer', user_id=user_id)

def other_transfer(request, user_id):
    if request.method == 'POST':
        source_account_id = request.POST.get('source_account_id')
        destination_account_id = request.POST.get('destination_account_id')
        amount = Decimal(request.POST.get('amount'))
        
        try:
            source_account = UserAccount.objects.get(accountNo=source_account_id, user_id=user_id)
            destination_account = UserAccount.objects.get(accountNo=destination_account_id)
            
            if source_account_id == destination_account_id:
                messages.error(request, 'Source and destination accounts cannot be the same.')
            elif source_account.balance < amount:
                messages.error(request, 'Insufficient balance in the source account.')
            else:
                source_account.balance -= amount
                source_account.save()
                destination_account.balance += amount
                destination_account.save()
                Transaction.objects.create(
                    transaction_id=generate_transaction_id(),
                    action='transfer',
                    debit=0,
                    credit=amount,
                    balance=source_account.balance,
                    other=f'Transferred to {destination_account_id}',
                    user_id=source_account.user_id,
                    account=source_account
                )
                Transaction.objects.create(
                    transaction_id=generate_transaction_id(),
                    action='transfer',
                    debit=amount,
                    credit=0,
                    balance=destination_account.balance,
                    other=f'Received from {source_account_id}',
                    user_id=destination_account.user_id,
                    account=destination_account
                )
                messages.success(request, 'Funds transferred successfully!')
        except UserAccount.DoesNotExist:
            messages.error(request, 'One of the accounts does not exist!')
        except Exception:
            messages.error(request, 'An error occurred while processing the transfer.')
        
        return redirect('external_transfer', user_id=user_id)
    else:
        return redirect('external_transfer', user_id=user_id)

def create_account_request(request, user_id):
    user_accounts = UserAccount.objects.filter(user_id=user_id)
    total_balance = calculate_total_balance(user_id)
    context = {
        'user_id': user_id,
        'user_accounts': user_accounts,
        'total_balance': total_balance,
    }
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        account_type = request.POST.get('account_type')
        user_details = Customer.objects.get(user_id=user_id)
        notice_text = f"Account request received for user {user_details.username}. Account type: {account_type}"
        Notification.objects.create(user_id=user_details, notice=notice_text)
        messages.success(request, 'Request sent. It may take a while to get approved.')
        return render(request, 'usr_accounts.html', context)
    else:
        return render(request, 'usr_accounts.html', context)

def notifications(request, mgr_id):
    notifications = Notification.objects.all()  
    context = {
        'mgr_id': mgr_id,
        'notifications': notifications,
    }
    return render(request, 'notifications.html', context)

def delete_notification(request, mgr_id):
    notifications = Notification.objects.all()  
    context = {
        'mgr_id': mgr_id,
        'notifications': notifications,
    }
    if request.method == 'POST':
        notification_id = request.POST.get('notification_id')
        notification = Notification.objects.get(id=notification_id)
        notification.delete()
    return render(request, 'notifications.html', context)   