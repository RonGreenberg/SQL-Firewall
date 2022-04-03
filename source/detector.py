import sqlparse

class Detector:
    def __init__(self):
        self.detectedInjectionTypes = []

    def isInjected(self, query):
        ret = False
        ret = ret | self.check_stacking_queries(query) # preventing short-circuit evaluation
        ret = ret | self.check_comment_at_the_end(query)
        ret = ret | self.check_union(query)
        return ret

    def check_stacking_queries(self, query):
        splitted = sqlparse.split(query)
        if len(splitted) > 1:
            self.detectedInjectionTypes.append("Stacking queries - trying to run additional queries")
            return True
        return False

    def check_comment_at_the_end(self, query):
        parsed = sqlparse.parse(query)[0]
        last_token = parsed.tokens[-1]
        if str(last_token.value).find("--") != -1:
            self.detectedInjectionTypes.append("Comment at the end of statement")
            return True
        return False
        # for token in parsed.tokens:
        #     if isinstance(token, sqlparse.sql.Where) and str(token.value).find("--") != -1:
        # #if query.find("--") != -1:
        #         print("SQL Injection detected! Comment at the end of statement")

    def check_union(self, query):
        parsed = sqlparse.parse(query)[0]
        for token in parsed.tokens:
            if token.ttype == sqlparse.tokens.Keyword and str(token.value).upper() == "UNION":
                self.detectedInjectionTypes.append("Union set - Adding UNION to read from another table")
                return True
        return False

detector = Detector()
detector.isInjected("SELECT first_name, last_name, email FROM members WHERE username='admin' -- ' AND showpublic=1")
print(detector.detectedInjectionTypes)

detector = Detector()
detector.isInjected("select col1  from table1 where col1 > 1 union select col2 from table2")
print(detector.detectedInjectionTypes)

detector = Detector()
detector.isInjected("SELECT name, description FROM products WHERE category = 'Gifts' UNION SELECT username, password FROM users--")
print(detector.detectedInjectionTypes)
