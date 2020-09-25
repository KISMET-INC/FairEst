from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import bcrypt
from datetime import *


#---------------------------------------------##
# GLOBAL RENDERS
#
#---------------------------------------------##
#=============================================##
# read_all()
# RENDERS table to see all users in database
# with the ability to delete users
#=============================================##
def read_all(request):
    context = {
        'users': User.objects.all()
    }
    return render(request,'example_templates/read_all.html',context)

#=============================================##
# logout()
# Deletes the session keys and 
# REDIRECTS to root
#=============================================##
def signout(request):
    request.session.flush()
    return redirect('/')




#---------------------------------------------##
# GLOBAL PROCESSES
#
#---------------------------------------------##


#=============================================##
# process_signin()
# PROCESSES process_signin request
# REDIRECTS back to root with errors or
# to process_signin page on success
#=============================================##
def process_signin(request):
    post = request.POST
    errors = User.objects.signin_validator(post)
    
    if len(errors) > 0:
        for value in errors.values():
            messages.error(request,value, extra_tags='signin')
        return redirect('/')

    # No errors set session keys
    user_email_query = User.objects.filter(email = post['email'])
    this_user = User.objects.get(id=user_email_query[0].id)

    request.session['user_id'] = this_user.id
    request.session['user_name'] = this_user.first_name

    return redirect('/main_page')


#=============================================##
# process_remove_user()
# PROCESSES the deletion of a user in the
# database.  REDIRECTS to read_all table
#=============================================##
def process_remove_user(request, user_id):
    this_user = User.objects.get(id = user_id)
    this_user.delete()
    return redirect('/read_all')


#=============================================##
# process_register()
# return redirect('/')
#=============================================##
def process_register(request):
    post = request.POST
    errors = User.objects.register_validator(post)
    
    if len(errors) > 0:
        for value in errors.values():
            messages.error(request,value, extra_tags='reg')
        return redirect('/')
    
    # No errors - create user  and set session keys
    hash = bcrypt.hashpw(post['pass'].encode(), bcrypt.gensalt()).decode()
    User.objects.create(first_name=post['first'], last_name=post['last'], password = hash, bday = post['bday'], email = post['email'])
    new_user = User.objects.last()

    request.session['user_id'] = new_user.id
    request.session['user_name'] = new_user.first_name
    return redirect('/main_page')












#/////////////////////////////////////////////##
# PROJECT SPECIFIC RENDERS
#w
#/////////////////////////////////////////////##
#=============================================##
# landing()
# RENDERS login_reg.html
#=============================================##
def landing(request):

    coats = Coat_Type.objects.all()
    if len(coats) == 0 :
        print('initializing coat types...')
        #Generate Coat Types table
        coat_types = [
    {'name' : 'Clippable','desc' : 'Catch all for any breed whos hair must be clipped or scissored because it continues to  grow in lengh. Like human hair','examples': 'Yorkshire, Cocker, Lhasa, ShihTzu, Terriers '},
    {'name' : 'Doodle','desc' : 'An unusual category for labradoodles and standard poodles and any dog 30lbs and above  whos body is tall but low in mass and the coat is traditionally kept long.','examples': 'Standard Poodle, Labradoodle,   Wheaten Terriers, Afghans '},
    {'name' : 'Slick','desc' : 'Very short, slick, so short that hairs cannot be lifted away from body with your hands',    'examples': 'Doberman, American Pit Bull Terrier, Chihuahua'},
    {'name' : 'Short','desc' : 'Medium length. Sheds single thick rigid strands. Hair car be lifted away from body to   expose the skin.','examples': 'Labrador, Rottweiler, Beagle'},
    {'name' : 'Medium','desc' : 'Relatively thin. Long hairs usually grow on the fringes of the dog. Has a mild shedding    undercoat but never gets very dense','examples': 'Working border collies '},
    {'name' : 'Double','desc' : 'Dense undercoat, Medium length. Sheds dense clumps of fur.','examples': 'Siberian Husky,   Klekai, Welsh Corgi'},
    {'name' : 'Long Double','desc' : 'Dense undercoat, long flowing overcoat. Hairs over 3 inches long or longer',  'examples': 'Chow, Pomeranian, Samoyed, Australian Shepherd '}
    ]

        for i in coat_types:
            Coat_Type.objects.create(name = i['name'], desc = i['desc'], examples = i['examples'])


    if len(Price_Book.objects.all()) == 0 :
        print('initializing price_book..')
        Price_Book.objects.create()
    
    price_book = Price_Book.objects.get(id=1)

    services = Service.objects.all()
    if len(services) == 0:
        print('initializing services..')
        Service.objects.create(name = "Bath", price = 0, price_book = price_book)
        Service.objects.create(name = "Short Haircut", price = 10, price_book = price_book)
        Service.objects.create(name = "Long Haircut", price = 15, price_book = price_book)

    return render(request,'home.html')



#=============================================##
# coat_type()
#=============================================##
def coat_types(request):
    post = request.POST
    print(post)
    # if 'user_id' not in request.session:
    #     return redirect('/')
    context = {
    'first_batch' : Coat_Type.objects.all()[:3],
    'second_batch' : Coat_Type.objects.all()[3:]
    
    }
    return render(request,'coat_types.html',context)

#=============================================##
# dashboard()
#=============================================##
def dashboard(request):
    post = request.POST
    print(post)
    
    # if 'user_id' not in request.session:
    #     return redirect('/')
    

    context = {
        'owners' : Owner.objects.all(),
        'search' : None
        
        
    }

    return render(request,'dashboard.html', context)



#-------------------SEARCH-----------------------#
#=============================================##
# process_search()
# return redirect('/')
#=============================================##
def search(request):
    post = request.POST
    print(post)
    search_by = post['search_by']
    
    
    context = {
        'owners' : Owner.objects.all(),
        'search' : Owner.objects.filter(**{search_by :post['search']})
        
    }



    return render(request,'dashboard.html', context)

#-----------------OWNER-----------------------#

#=============================================##
# add_owner()
#=============================================##
def add_owner(request):
    post = request.POST
    print(post)
    
    # if 'user_id' not in request.session:
    #     return redirect('/')

    return render(request,'add_owner.html')


#=============================================##
# edit_owner()
#=============================================##
def edit_owner(request, owner_id,redirect_key, quote_id, estimate_id):
    post = request.POST
    print(owner_id)
    print(post)
    
    # if 'user_id' not in request.session:
    #     return redirect('/')
    
    #-------------------#

    context = {
        'owner' : Owner.objects.get(id = owner_id), 
        'redirect_key': redirect_key,
        'quote_id': quote_id,
        'estimate_id': estimate_id
    }

    return render(request,'edit_owner.html',context)

#=============================================##
# show_owner_info()
#=============================================##
def show_owner_info(request, owner_id):
    post = request.POST
    print(post)
    
    # if 'user_id' not in request.session:
    #     return redirect('/')
    # #-------------------#
    owner = Owner.objects.get(id = owner_id)

    context = {
        'owner':  Owner.objects.get(id = owner_id),
        'coats': Coat_Type.objects.all()

    }
    return render(request,'show_owner_info.html',context)




#-------------------DOGS-----------------------#

#=============================================##
# add_a_dog_to_owner()
#=============================================##
def add_dog_to_owner(request, owner_id):
    post = request.POST
    print(post)
    
    # if 'user_id' not in request.session:
    #     return redirect('/')
    # #-------------------#

    
    context = {
        'coats' : Coat_Type.objects.all(),
        'owner':  Owner.objects.get(id = owner_id),
    }

    return render(request,'add_dog_to_owner.html', context)

#=============================================##
# edit_dog()
#=============================================##
def edit_dog(request, dog_id):
    post = request.POST
    print(post)
    
    # if 'user_id' not in request.session:
    #     return redirect('/')
    # #-------------------#

    context = {
        'dog' : Dog.objects.get(id = dog_id),
        'coats' : Coat_Type.objects.all()
    }

    return render(request,'edit_dog.html',context)


#=============================================##
# show_dog_info()
#=============================================##
def show_dog_info(request, dog_id):
    post = request.POST
    print(post)
    
    # if 'user_id' not in request.session:
    #     return redirect('/')
    # #-------------------#
    context = {
        'dog' : Dog.objects.get(id=dog_id)

    }
    return render(request,'show_dog_info.html',context)


#-------------------ESTIMATES-----------------------#


#=============================================##
# add_quotes_to_estimate()
#=============================================##
def add_quotes_to_estimate(request,estimate_id):
    post = request.POST
    print(post)
    print(estimate_id)
    
    # if 'user_id' not in request.session:
    #     return redirect('/')
    # #-------------------#

    estimate = Estimate.objects.get(id=estimate_id)

    context = {
        'coats' : Coat_Type.objects.all(),
        'estimate' : Estimate.objects.get(id=estimate_id),
        'owner' : Owner.objects.get(id=estimate.owner.id),
        'services': Service.objects.all()
    }

    return render(request,'add_quotes_to_estimate.html', context)

#=============================================##
# create_first_estimate()
#=============================================##
def add_first_estimate(request):
    post = request.POST
    print(post)
    
    # if 'user_id' not in request.session:
    #     return redirect('/')
    # #-------------------#
    context = {
        'services' : Service.objects.all(),
        'coats' : Coat_Type.objects.all()
    }
    return render(request,'add_first_estimate.html',context)

#=============================================##
# add_first_estimate_to_owner()
#=============================================##
def add_first_estimate_to_owner(request, owner_id):
    post = request.POST
    print(post)
    this_owner = Owner.objects.get(id=owner_id)
    estimate = Estimate.objects.create(this_owner)
    # if 'user_id' not in request.session:
    #     return redirect('/')
    # #-------------------#
    
    return render(request,'add_first_estimate_to_owner.html',context)

#-------------------QUOTES-----------------------#

#=============================================##
# edit_quote()
#=============================================##
def edit_quote(request, quote_id, redirect_key, estimate_id):
    post = request.POST
    print(post)
    print(estimate_id)
    # if 'user_id' not in request.session:
    #     return redirect('/')
    # #-------------------#
    quote = Quote.objects.get(id=quote_id)
    dog = Dog.objects.get(id = quote.dog.id)
    context = {
        'quote' : Quote.objects.get(id=quote_id),
        'coats' : Coat_Type.objects.all(),
        'dog' : dog,
        'estimate_id': estimate_id,
        'redirect_key':redirect_key,
        'services' : Service.objects.all()
    }
    return render(request,'edit_quote.html',context)

#=============================================##
# add_quote_to_dog()
#=============================================##
def add_quote_to_dog(request, dog_id):
    post = request.POST
    print(post)
    
    # if 'user_id' not in request.session:
    #     return redirect('/')
    # #-------------------#
    dog = Dog.objects.get(id = dog_id)
    context = {
        'coats' : Coat_Type.objects.all,
        'dog' : dog,
    }
    return render(request,'add_quote_to_dog.html',context)


#-------------------EXTRAS-----------------------#
#=============================================##
# add_extras_to_quote()
#=============================================##
def add_extras_to_quote(request, quote_id, estimate_id):
    post = request.POST
    print(post)
    
    # if 'user_id' not in request.session:
    #     return redirect('/')
    # #-------------------#
    quote = Quote.objects.get(id = quote_id)
    context = {
        'coats' : Coat_Type.objects.all(),
        'owner' : Owner.objects.get(id=quote.owner.id),
        'quote' : quote
    }
    if estimate_id != 0:
        context['estimate'] = Estimate.objects.get(id=estimate_id)

    return render(request,'add_extras_to_quote.html',context)





#/////////////////////////////////////////////##
# PROJECT SPECIFIC PROCESSES
#
#/////////////////////////////////////////////##

#=============================================##
# init_db_objects()
#=============================================##
def init_db_objects(request):
    post = request.POST
    print(post)


    return redirect('/dashboard')


#=============================================##
# process_add_owner()
# return redirect('/')
#=============================================##
def process_add_owner(request):
    post = request.POST
    print(post)
    Owner.objects.create(first = post['first'], last = post['last'], email = post['email'], phone = post['phone'], notes = post['notes'])
    print('Creating new owner object...')

    return redirect('/dashboard')



#=============================================##
# process_edit_owner()
# return redirect('/')
#=============================================##
def process_edit_owner(request, owner_id, redirect_key, quote_id, estimate_id):
    post = request.POST
    print(owner_id)
    print(f'est_id {estimate_id}')

    this_owner = Owner.objects.get(id = owner_id)

    this_owner.first = post['first']
    this_owner.last = post['last']
    this_owner.email = post['email']
    this_owner.phone = post['phone']
    this_owner.notes = post['notes']

    this_owner.save()

    if redirect_key == 0:
        return redirect('/dashboard')
    
    if redirect_key == 1:
        return redirect(f'/add_quotes_to_estimate/{estimate_id}')
    
    if redirect_key == 2:
        return redirect(f'/edit_quote/{quote_id}/{redirect_key}/{estimate_id}')
    

#=============================================##
# process_delete_owner()
# return redirect('/')
#=============================================##
def process_delete_owner(request, owner_id):
    post = request.POST
    print(owner_id)

    this_owner = Owner.objects.get(id = owner_id)
    this_owner.delete()

    return redirect('/dashboard')

#-------------------DOGS-----------------------#

#=============================================##
# process_add_quote_to_estimate
# return redirect('/')
#=============================================##
def process_add_quote_to_estimate(request, estimate_id):
    post = request.POST
    print(post)
    errors = Dog.objects.split_quote_validator(post)
    
    if len(errors) > 0:
        for value in errors.values():
            messages.error(request,value, extra_tags='reg')
        return redirect(f'/add_quotes_to_estimate/{estimate_id}')

    #Getting objects together
    this_estimate = Estimate.objects.get(id=estimate_id)
    this_owner = Owner.objects.get(id=this_estimate.owner.id)

    if(post['pet_name'] != ''):
        this_price_book = Price_Book.objects.get(id=1)
        bath_service = Service.objects.get(name = 'Bath')
        coat = Coat_Type.objects.get(id = post['coat_type'])

        this_dog = Dog.objects.create(name = post['pet_name'], weight = post['weight'], coat = coat, notes=post['notes'], owner=this_owner)
        this_dog.save()

        new_quote = Quote.objects.create(price_book = this_price_book, service = bath_service, dog = this_dog, owner=this_owner)
        new_quote.setExtras(post['overdue'],post['special'], post['profuse'], post['dematting'])
        new_quote.save()
        this_estimate.quotes.add(new_quote)

    
    if 'quote_id' in request.POST:
        
        for quote in request.POST.getlist('quote_id'):
            print(quote)
            this_estimate.quotes.add(Quote.objects.get(id=quote))

    return redirect(f'/add_quotes_to_estimate/{estimate_id}')

#=============================================##
# process_remove_dog()
# return redirect('/')
#=============================================##
def process_remove_dog(request, dog_id, redirect_key, quote_id, estimate_id):
    post = request.POST
    
    this_dog = Dog.objects.get(id=dog_id)
    owner = Owner.objects.get(id = this_dog.owner.id)
    this_dog.delete()

    return redirect(f'/edit_owner/{owner.id}/{redirect_key}/{quote_id}/{estimate_id}')

#=============================================##
# process_remove_dog()
# return redirect('/')
#=============================================##
def process_remove_dog_from_estimate(request, quote_id,estimate_id):
    post = request.POST

    quote = Quote.objects.get(id=quote_id)
    this_estimate = Estimate.objects.get(id=estimate_id)

    this_estimate.quotes.remove(quote)

    return redirect(f'/add_quotes_to_estimate/{estimate_id}')
#=============================================##
# process_edit_dog()
# return redirect('/')
#=============================================##
def process_edit_dog(request, dog_id):
    post = request.POST
    print(post)
    new_coat = Coat_Type.objects.get(id = post['coat_type'])
    this_dog = Dog.objects.get(id=dog_id)
    this_dog.name = post['name']
    this_dog.weight = post['weight']
    this_dog.coat = new_coat
    this_dog.notes = post['notes']
    this_dog.save()

    return redirect(f'/show_owner_info/{this_dog.owner.id}')

    #-------------------ESTIMATE-----------------------#


#-------------------ESTIMATES-----------------------#
#=============================================##
# process_add_first_estimate
# return redirect('/')
#=============================================##
def process_add_first_estimate(request):
    post = request.POST
    print(post)
    errors = Dog.objects.dog_validator(post)
    
    if len(errors) > 0:
        for value in errors.values():
            messages.error(request,value, extra_tags='reg')
        return redirect('/add_first_estimate')

    this_owner = Owner.objects.create(first=post['first'], last = post['last'], email = post['email'], notes =post['notes'])
    this_estimate = Estimate.objects.create(owner = this_owner)

    this_price_book = Price_Book.objects.get(id=1)
    service = Service.objects.get(name = post['service'])
    coat = Coat_Type.objects.get(id = post['coat_type'])

    this_dog = Dog.objects.create(name = post['pet_name'], weight = post['weight'], coat = coat, notes=post['notes'], owner=this_owner)

    new_quote = Quote.objects.create(price_book = this_price_book, service = service, dog = this_dog, owner=this_owner)
    new_quote.setExtras(post['overdue'],post['special'], post['profuse'], post['dematting'])

    # new_quote.calc_weight_price()
    # new_quote.calc_coat_price()
    # new_quote.save()

    this_estimate.quotes.add(new_quote)

    return redirect(f'/add_quotes_to_estimate/{this_estimate.id}')

#=============================================##
# /process_delete_estimate()
# return redirect('/')
#=============================================##
def process_delete_estimate(request, estimate_id):
    post = request.POST
    this_estimate = Estimate.objects.get(id=estimate_id)
    this_estimate.delete()

    return redirect('/dashboard')

#=============================================##
# process_add_estimate_to_owner()
# return redirect('/')
#=============================================##
def process_add_estimate_to_owner(request, owner_id):
    post = request.POST
    print(post)

    this_owner = Owner.objects.get(id = owner_id)
    new_estimate = Estimate.objects.create(start_price = request.session['start_price'], owner = this_owner)
    if post['weight'] !='':
        process_add_quote_to_estimate(request, new_estimate.id)

    
    for i in request.POST.getlist('dog_id'):
        quote = Quote.objects.get(id=i)
        new_estimate.quotes.add(quote)


    return redirect(f'/show_owner_info/{owner_id}')

#=============================================##
# /process_add_first_estimate_to_owner()
# return redirect('/')
#=============================================##
def process_add_first_estimate_to_owner(request,owner_id):
    post = request.POST
    this_owner = Owner.objects.get(id = owner_id)
    this_estimate = Estimate.objects.create(owner = this_owner)
    
    return redirect(f'/add_quotes_to_estimate/{this_estimate.id}')








#-------------------QUOTE-----------------------#

#=============================================##
# process_edit_quote()
# return redirect('/')
#=============================================##
def process_edit_quote(request,quote_id, redirect_key, estimate_id):
    post = request.POST
    print(post)

    print(post)
    errors = Dog.objects.quote_validator(post)
    
    if len(errors) > 0:
        for value in errors.values():
            messages.error(request,value)
        return redirect(f'/edit_quote/{quote_id}/{redirect_key}/{estimate_id}')

    coat = Coat_Type.objects.get(id = int(post['coat_type']))
    this_quote = Quote.objects.get(id = quote_id)
    this_dog = Dog.objects.get(id= this_quote.dog.id)
    this_dog.name = post['pet_name'] 
    this_dog.weight = post['weight']
    this_dog.coat = coat
    this_dog.notes = post['notes']
    this_dog.save()
    
    service = Service.objects.get(name = post['service'])
    print(service.name)
    this_quote.dog = this_dog
    this_quote.service = service
    print(this_quote.service.price)
    this_quote.calc_coat_price()
    this_quote.calc_weight_price()
    this_quote.setExtras(post['overdue'],post['special'], post['profuse'], post['dematting'])
    this_quote.set_service_price()
    this_quote.save()

    if redirect_key == 0:
        return redirect(f'/dashboard')

    else:
        return redirect(f'/add_quotes_to_estimate/{estimate_id}')

#=============================================##
# process_add_quote_to_dog()
# return redirect('/')
#=============================================##
def process_add_quote_to_dog(request,dog_id):
    post = request.POST


    return redirect('/add_quote_to_dog')

#-------------------EXTRAS-----------------------#
#=============================================##
# process_add_extras_to_quote()
# return redirect('/')
#=============================================##
def process_add_extras_to_quote(request,quote_id, estimate_id):
    post = request.POST
    print(post)
    
    service = Service.objects.get(name = post['service'])
    this_quote = Quote.objects.get(id = quote_id)
    this_quote.service = service
    this_quote.setExtras(post['overdue'], post['special'], post['profuse'], post['dematting'])
    this_quote.save()




    return redirect(f'/add_quotes_to_estimate/{estimate_id}')