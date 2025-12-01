

def where_to(state, too):
    if state == "first":
        if too == "second":
            first_to_second()
                        
        if too == "third":
            first_to_second()
            second_to_third()
            
        if too == "forth":
            first_to_second()
            second_to_third()
            third_to_forth()
            
       
    
    elif state == "second":
        if too == "first":
            second_to_first()
            
        if too == "third":
            second_to_third()
            
        if too == "forth":
            second_to_third()
            third_to_forth()
            
        
    
    elif state == "third":
        if too == "first":
            third_to_second()
            second_to_first()
            
        if too == "second":
            third_to_second()
            
            
        if too == "forth":
            third_to_forth()
            
       
    
    elif state == "forth":
        if too == "first":
            forth_to_third()
            third_to_second()
            second_to_first()
            
        if too == "second":
            forth_to_third()
            third_to_second()
        
        if too == "third":
            forth_to_third()
