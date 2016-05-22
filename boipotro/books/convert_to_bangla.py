# -*- coding: utf-8 -*-

def convert_number_in_bangla(number):
    temp=str(number)
    ret="";
    for i in range(0,len(temp)):
        if (temp[i]=='1'):
            ret=ret+'১'
        elif (temp[i]=='2'):
            ret=ret+'২'
        elif (temp[i]=='3'):
            ret=ret+'৩'
        elif (temp[i]=='4'):
            ret=ret+'৪'
        elif (temp[i]=='5'):
            ret=ret+'৫'
        elif (temp[i]=='6'):
            ret=ret+'৬'
        elif (temp[i]=='7'):
            ret=ret+'৭'
        elif (temp[i]=='8'):
            ret=ret+'৮'
        elif (temp[i]=='9'):
            ret=ret+'৯'
        elif (temp[i]=='0'):
            ret=ret+'০'
        else:
            ret=ret+temp[i]
    return ret
