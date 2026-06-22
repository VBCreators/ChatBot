

def check_password_match(user_password, re_user_password):
    if user_password == re_user_password :
        return True
    else:
        return False        


def check_user_signup(user_name, user_password):

    try :
        
        if not user_name:
            return False
        
        if not user_password:
            return False

        

        return True

    except Exception :
        return False

    
    

