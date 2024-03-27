def reciprocal( num1 ):  
    try:  
        reci = 1 / num1  
    except ZeroDivisionError:  
        print( "We cannot divide by zero" )  
    else:  
        print ( reci )  
# Calling the function and passing values  
reciprocal( 4 )  
reciprocal( 0 )  