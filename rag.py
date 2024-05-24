class Prag:
    def __init__(self, llm, vdb,enc) :
        
        self.enc = enc
        self.llm = llm
        self.vdb = vdb

    
    def respond(self, query):
        resultDict = self.vdb.query(query)
        s=set()
        titles="\nSource documents:\n\n"
        for i in resultDict:
            curr=i["title"]
            if curr not in s:
                s.add(curr)
                titles+=curr+"\n"

        


        prompt = f"""
        Below is a question and a context. Your job is to answer the question based on the context paragraphs 
        and respond to the questions with relevant information.
        Question: {query}
        Context: {[i.get("text","") for i in resultDict]}
        """

        for a in self.llm.respond(prompt):
            if a=="[DONE]":
                yield titles
            yield a