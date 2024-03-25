from django.db import models
from django.core.validators import RegexValidator


class Branch(models.Model):
    branchNo = models.CharField(max_length=111)
    branchName = models.CharField(max_length=111, primary_key=True)
    branchAddress = models.CharField(max_length=111)

    def __str__(self):
        return self.branchName



class Login(models.Model):
    email = models.CharField(max_length=111)
    password = models.CharField(max_length=111)
    type = models.CharField(max_length=111)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email



class Customer(models.Model):
    user_id = models.CharField(max_length=255, primary_key=True)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.EmailField()
    contact_number = models.CharField(max_length=20)
    address = models.TextField()

    def __str__(self):
        return self.user_id
    
class Manager(models.Model):
    mgr_id = models.CharField(max_length=255, primary_key=True)
    mgrname = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.EmailField()
    def __str__(self):
        return self.mgr_id
    
class UserAccount(models.Model):
    accountNo = models.CharField(max_length=10, primary_key=True, unique=True, validators=[RegexValidator(r'^[0-9]+$')])
    user_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    email = models.EmailField()
    name = models.CharField(max_length=111)
    balance = models.DecimalField(max_digits=15, decimal_places=2)
    number = models.CharField(max_length=111)
    city = models.CharField(max_length=111)
    address = models.CharField(max_length=111)
    source = models.CharField(max_length=111)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    ACCOUNT_TYPE_CHOICES = [
        ('savings', 'Savings'),
        ('current', 'Current'),
        ('salary', 'Salary'),
    ]
    accountType = models.CharField(max_length=7, choices=ACCOUNT_TYPE_CHOICES)
    date = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return str(self.accountNo)
    
class Notification(models.Model):
    user_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    notice = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notice for Customer {self.user_id}"

class Transaction(models.Model):
    ACTION_CHOICES = [
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
        ('transfer', 'Transfer')
    ]
    
    transaction_id = models.CharField(max_length=10, primary_key=True)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    credit = models.DecimalField(max_digits=15, decimal_places=2)
    debit = models.DecimalField(max_digits=15, decimal_places=2)
    balance = models.DecimalField(max_digits=15, decimal_places=2)
    other = models.CharField(max_length=111)
    user_id = models.ForeignKey(Customer, on_delete=models.CASCADE) 
    account = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction {self.transaction_id}"



class Bank(models.Model):
    # Represents the banking institution
    # Attributes: None (Assumed to be a single entity in the system)
    pass

