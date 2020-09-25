from django.urls import path
from . import views
urlpatterns = [
    

    #---------------------------------------------##
    # GLOBAL RENDERS
    #---------------------------------------------##
    path('',views.landing),
    # path('main_page', views.main_page),
    path('signout', views.signout),
    path('read_all',views.read_all),
    #---------------------------------------------##
    # GLOBAL PROCESSES
    #---------------------------------------------##
    path('process_register', views.process_register),
    path('process_signin', views.process_signin),
    path('process_remove_user', views.process_remove_user),

    #=============================================##
    # RENDERS
    #=============================================##
    path('coat_types', views.coat_types),
    path('dashboard', views.dashboard),
    #OWNER
    path('add_owner', views.add_owner),
    path('edit_owner/<int:owner_id>/<int:redirect_key>/<int:quote_id>/<int:estimate_id>', views.edit_owner),
    path('show_owner_info/<int:owner_id>', views.show_owner_info),
    #DOG
    path('show_dog_info/<int:dog_id>', views.show_dog_info),
    path('add_dog_to_owner/<int:owner_id>', views.add_dog_to_owner),
    path('edit_dog/<int:dog_id>', views.edit_dog),
    #ESTIMATE
    path('add_first_estimate_to_owner/<int:owner_id>', views.add_first_estimate_to_owner),
    path('add_quotes_to_estimate/<int:estimate_id>', views.add_quotes_to_estimate),
    path('add_first_estimate', views.add_first_estimate),

    # SEARCH
    path('search', views.search),

    #QUOTE
    path('add_quote_to_dog/<int:dog_id>', views.add_quote_to_dog),
    path('edit_quote/<int:quote_id>/<int:redirect_key>/<int:estimate_id>', views.edit_quote),

    #EXTRAS
    path('add_extras_to_quote/<int:quote_id>/<int:estimate_id>', views.add_extras_to_quote),


    #=============================================##
    # PROCESSES
    #=============================================##
    path('init_db_objects', views.init_db_objects),
    #OWNER
    path('process_add_owner', views.process_add_owner),
    path('process_edit_owner/<int:owner_id>/<int:redirect_key>/<int:quote_id>/<int:estimate_id>', views.process_edit_owner),
    path('process_delete_owner/<int:owner_id>', views.process_delete_owner),
    #DOG
    path('process_remove_dog/<int:dog_id>/<int:redirect_key>/<int:quote_id>/<int:estimate_id>', views.process_remove_dog),
    path('process_remove_dog_from_estimate/<int:quote_id>/<int:estimate_id>', views.process_remove_dog_from_estimate),
    path('process_edit_dog/<int:dog_id>', views.process_edit_dog),

    #ESTIMATE
    path('process_delete_estimate/<int:estimate_id>', views.process_delete_estimate),
    path('process_add_quote_to_estimate/<int:estimate_id>', views.process_add_quote_to_estimate),
    path('process_add_first_estimate', views.process_add_first_estimate),
    path('process_add_estimate_to_owner/<int:owner_id>', views.process_add_estimate_to_owner),
    path('process_add_first_estimate_to_owner/<int:owner_id>', views.process_add_first_estimate_to_owner),

    #QUOTE
    path('process_edit_quote/<int:quote_id>/<int:redirect_key>/<estimate_id>', views.process_edit_quote),
    path('process_add_quote_to_dog/<int:dog_id>', views.process_add_quote_to_dog),

    #EXTRAS
    path('process_add_extras_to_quote/<int:quote_id>/<int:estimate_id>', views.process_add_extras_to_quote),

    
]

    