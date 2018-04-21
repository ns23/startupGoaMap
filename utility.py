import string

def empty_file(filename):
    open(filename, 'w').close()
    pass

def format_company_name(cname):
   cname = cname.replace('(', '')
   cname = cname.replace(')', '')
   cname = cname[:-1]
   cname = cname.rstrip(string.digits)
   cname = cname.strip()
   return cname
