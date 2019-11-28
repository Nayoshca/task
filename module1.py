s = [1,2,3,4,5,6,7,8,9]


pi = 5-1
pj =5-1
pk =5-1
s= s[pi:]

for i,item in enumerate(s):
    print("i")
    print(i,item)
    
    d = [1,2,3,4,5,6,7,8,9]
    if(i==0):
        d = d[pi:]
   
  
    for j,item in enumerate(d):
        print("j ")
        print(j,item)
        
        f = [1,2,3,4,5,6,7,8,9]
        if(i==0 and j==0):
            f = f[pk:]

       
        
        for k,item in enumerate(f):
                print("k ")
                print(k,item)
                
