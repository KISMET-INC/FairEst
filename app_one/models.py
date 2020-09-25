from django.db import models
from datetime import *
import re
import bcrypt




#---------------------------------------------##
# VALIDATORS
#---------------------------------------------##

class UserManager(models.Manager):
    #=============================================##
    # register_validator()
    #=============================================##
    def register_validator(self, postData):
        print(postData)
        # easy use variable
        post = postData
        # empty error dictionary
        errors = {}

        # check first name length
        if len(post['first']) < 2:
            errors['first'] = 'First Name must be at least 2 characters'
        # check last name length
        if len(post['last']) < 2:
            errors['last'] = 'Last Name must be at least 2 characters'
        
        # password len
        if len(post['pass']) < 2:
            errors['passlen'] = 'Password must be at least 8 characters'
        
        # password match
        if post['pass'] != post['confirm']:
            errors['passmatch'] = 'Passwords do no match'

        # email format
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post['email']):    # test whether a field matches the pattern
            errors['email_format'] = "Problem with email address format."

        # email unique
        user_email_query = User.objects.filter(email = post['email'])
        if len(user_email_query) > 0:
            errors['email_take'] = "Email address taken."

        return errors

    #=============================================##
    # signin_validator 
    #=============================================##
    def signin_validator(self, postData):
        print(postData)
        #easy use variable
        post = postData
        # empty error dictionary
        errors = {}

        # password length
        if len(post['pass']) < 2:
            errors['passlen'] = 'Password must be at least 8 characters'
        
        # email format
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post['email']):    # test whether a field matches the pattern
            errors['email_format'] = "Problem with email address format."

        # email NOT located
        user_email_query = User.objects.filter(email = post['email'])
        if len(user_email_query) == 0:
            errors['email_pass_no_match'] = "Problem with email or password."

        else:
            this_user = User.objects.get(id=user_email_query[0].id)
            # email located - password check
            if bcrypt.checkpw(post['pass'].encode(), this_user.password.encode()) != True:
                errors['email_pass_no_match'] = "Problem with email or password."

        return errors


class DogManager(models.Manager):
    #=============================================##
    # dog_validator SPECIFIC
    # validates the data for user registration
    #=============================================##
    def dog_validator(self, postData):
        print(postData)
        #easy use variable
        post = postData
        # empty error dictionary
        errors = {}
        if len(post['last']) < 2:
            errors['last'] = 'Owner last name must be at least 2 characters'

        if len(post['pet_name']) < 2:
            errors['pet_name'] = 'Pet name must be at least 2 characters'

        if len(post['weight']) < 1:
            errors['weight'] = 'Pet weight must be included'

        elif post['weight'].isnumeric() == False:
            errors['weight_num'] = 'Pet weight must be a number'

        elif int(post['weight']) > 200:
            errors['weight_max'] = 'Pet weight must be 200lbs and under'

        return errors


    #=============================================##
    # dog_validator SPECIFIC
    # validates the data for user registration
    #=============================================##
    def quote_validator(self, postData):
        print(postData)
        #easy use variable
        post = postData
        # empty error dictionary
        errors = {}

        if len(post['pet_name']) < 2:
            errors['pet_name'] = 'Pet name must be at least 2 characters'

        if len(post['weight']) < 1:
            errors['weight'] = 'Pet weight must be included'

        elif post['weight'].isnumeric() == False:
            errors['weight_num'] = 'Pet weight must be a number'

        elif int(post['weight']) > 200:
            errors['weight_max'] = 'Pet weight must be 200lbs and under'

        return errors

    #=============================================##
    # dog_validator SPECIFIC
    # validates the data for user registration
    #=============================================##
    def split_quote_validator(self, postData):
        print(postData)
        #easy use variable
        post = postData
        # empty error dictionary
        errors = {}

        if post['button_press'] == 1:
            if len(post['pet_name']) < 2:
                errors['pet_name'] = 'Pet name must be at least 2 characters'

            if len(post['weight']) < 1:
                errors['weight'] = 'Pet weight must be included'

            elif post['weight'].isnumeric() == False:
                errors['weight_num'] = 'Pet weight must be a number'

            elif int(post['weight']) > 200:
                errors['weight_max'] = 'Pet weight must be 200lbs and under'

        return errors


#---------------------------------------------##
# MODELS
#---------------------------------------------##

class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    password = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    bday = models.DateField()
    # RELATIONSHIPS
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class Owner(models.Model):
    first = models.CharField(max_length=30, null = True)
    last = models.CharField(max_length=30)
    email = models.CharField(max_length=255, null = True)
    phone = models.CharField(max_length=255,null = True)
    notes = models.CharField(max_length=255, null = True)
    #OWNER.dogs  #BUCKET OF DOGS BELONGING TO THIS OWNER
    #OWNER.quotes 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Coat_Type(models.Model):
    name = models.CharField(max_length=30)
    desc = models.CharField(max_length=255)
    examples = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # COAT_TYPE.dogs - #BUCKET OF DOGS WITH THIS COAT TYPE



class Dog(models.Model):
    name = models.CharField(max_length=30)
    weight = models.IntegerField()
    years = models.IntegerField(null = True)
    months = models.IntegerField(null = True)
    notes = models.CharField(max_length=255, null = True)
    coat = models.ForeignKey(Coat_Type, related_name = 'dogs', on_delete = models.CASCADE)
    owner = models.ForeignKey(Owner, related_name = 'dogs', on_delete = models.CASCADE)
    # DOG.quotes #BUCKET of all the quotes for this dog
    estimate = models.ManyToManyField('Estimate', related_name = "dogs")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = DogManager()

    
    def updateDog(self,name,weight,coat,notes):
        self.name = name
        self.weight = weight
        self.coat = coat
        self.notes = notes



class Estimate(models.Model):
    owner = models.ForeignKey(Owner, related_name = 'estimates', on_delete= models.CASCADE)
    # ESTIMATE.quotes - # BUCKET OF QUOTES PER ESTIMATE (MTM)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    @property
    def total(self):
        total = 0;
        for quote in self.quotes.all():
            total += quote.total
        return total
    @property
    def total_dogs(self):
        return len(self.quotes.all())



class Service(models.Model):
    name = models.CharField(max_length=30)
    price = models.IntegerField()
    desc =  models.CharField(null = True, max_length=255)
    price_book = models.ForeignKey('Price_Book', related_name = 'services', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # SERVICE.quotes




class Quote(models.Model):

    price_book = models.ForeignKey('Price_Book', related_name = 'quotes', on_delete = models.CASCADE)
    service = models.ForeignKey(Service, related_name = "quotes", on_delete = models.CASCADE)
    dog = models.ForeignKey(Dog, related_name = 'quotes', on_delete = models.CASCADE)
    owner = models.ForeignKey(Owner, related_name = 'quotes', on_delete = models.CASCADE)
    overdue = models.IntegerField( default = 0 )
    special = models.IntegerField( default = 0)
    profuse = models.IntegerField( default = 0)
    dematting = models.IntegerField( default = 0)
    shedless = models.IntegerField(default = 0)
    service_price = models.IntegerField(default = 0)
    weight_price = models.IntegerField(null=True)
    coat_price = models.IntegerField(null=True)

    #quotes can exist on many estimates
    estimate = models.ManyToManyField(Estimate, related_name = "quotes")
    total = models.IntegerField( default = 0 )
    on_schedule = models.BooleanField(default = True)
    schedule_price =  models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def set_service_price (self):
        self.service_price = 0

        coat_haircut = {
                'Slick' : 0,
                'Short' : 20,
                'Medium' : 10,
                'Clippable' : 15,
                'Doodle' : 30,
                'Double' : 10,
                'Long Double' : 15,
            }
        
        if self.service.name == 'Short Haircut':
            for key,value in coat_haircut.items():
                if self.dog.coat.name == key:
                    self.service_price = value
        
        elif self.service.name == 'Long Haircut':
            for key,value in coat_haircut.items():
                if self.dog.coat.name == key:
                    self.service_price = value + 5
                    
        elif self.service.name == 'Bath' and self.dog.coat.name =='Doodle':
            self.service_price = 10
        
        else:
            
            self.service_price == 0


        return self.service_price




    def setTotal(self):
        if self.on_schedule == True:
            self.schedule_price = self.price_book.off_schedule
        else:
            self.schedule_price = 0
        self.total =  self.weight_price + self.coat_price  + self.overdue + self.schedule_price + self.overdue +self.special + self.profuse + self.dematting + self.service_price
        return self
    

    def setExtras(self,overdue, special, profuse, dematting):
        if overdue == '':
            overdue = 0

        if special == '':
            special = 0

        if profuse == '':
            profuse = 0

        if dematting == '':
            dematting = 0
        
        self.overdue = overdue
        self.special = special
        self.dematting = dematting
        self.profuse = profuse
        return self

    def calc_coat_price(self):
        coat_price = 0;
        coat_dict = {
            'Slick' : 0,
            'Short' : 5,
            'Medium' : 10,
            'Clippable' : 10,
            'Doodle' : 20,
            'Double' : 15,
            'Long Double' : 25,
        }

        for key,value in coat_dict.items():
            if self.dog.coat.name == key:
                self.coat_price = value + self.price_book.base_price

        return self.coat_price

    
    def calc_weight_price(self):
        weight_arr = [0,0,0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90]
        self.weight_price = weight_arr[round(int(self.dog.weight)/10)]
        return self.weight_price

    def __init__(self,*args, **kwargs):
        super(Quote,self).__init__(*args, **kwargs)
        self.calc_coat_price()
        self.calc_weight_price()
        self.set_service_price()
        self.setTotal()


class Price_Book(models.Model):
    base_price = models.IntegerField(default = 25)
    off_schedule =  models.IntegerField(default = 5)
    clean_feet =  models.IntegerField(default = 5)
    short_haircut =  models.IntegerField(default = 10)
    scissor_haircut =  models.IntegerField(default = 15)
    special_handling  = models.IntegerField(default = 10)
    shedless =  models.IntegerField(default = 15)


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)









