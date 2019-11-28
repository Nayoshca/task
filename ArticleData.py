class ArticleData:
    Article_Name=''
    Article_description =''
    Article_keywords = ''
    Article_category = ''
    Article_Sub_category = ''
    Article_views=''
    Article_index=''
    Article_ref=''
    Article_text=''
  

   
      
    def display(self): 
        print("Article_Name= " + self.Article_Name)
        print("Article_description ="+ self.Article_description )
        print("Article_keywords = " + self.Article_keywords)
        print("Article_category = " + self.Article_category)
        print("Article_Sub_category = " + self.Article_Sub_category)
        print("Article_views=" + str(self.Article_views))
        print("Article_index=" + self.Article_index)
        print("Article_ref=" + self.Article_ref)
        print("Article_text=" + self.Article_text)
        
