import sqlparse
import configparser


class Detector:
    def __init__(self):
        self.detectedInjectionTypes = []

    def isInjected(self, query):
        config = configparser.ConfigParser()
        config.read('configurations.ini')
        ret = False
        if (config['DetectionSettings']['check_stacking_queries'] == "true"):
            ret = ret | self.check_stacking_queries(query) # preventing short-circuit evaluation
        if (config['DetectionSettings']['check_comment_at_the_end'] == "true"):
            ret = ret | self.check_comment_at_the_end(query)
        if (config['DetectionSettings']['check_union'] == "true"):
            ret = ret | self.check_union(query)
        if (config['DetectionSettings']['check_always_true'] == "true"):
            ret = ret | self.check_always_true(query)
        if (config['DetectionSettings']['check_always_false'] == "true"):
            ret = ret | self.check_always_false(query)
        if (config['DetectionSettings']['check_if_blocked_keyword'] == "true"):
            ret = ret | self.check_if_blocked_keyword(query)
        if (config['DetectionSettings']['check_if_blocked_literal'] == "true"):
            ret = ret | self.check_if_blocked_literal(query)
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

    def check_always_true(self, query):
        query = str(query)
        or_index = query.find(" OR ")
        if or_index == -1:
            or_index = query.find(" or ")
            if or_index == -1:
                return False
        conditions = query[or_index:len(query)]
        parsed = sqlparse.parse(conditions)[0]
        comparison = str(find_next_comparison(parsed))
        # if comparison == "''=''":
        #     self.detectedInjectionTypes.append("''='' is always true")
        #     return True
        comparison_modified = comparison.replace("=", "==")
        comparison_modified = comparison_modified.replace("<>", "!=")
        try:
            if eval(comparison_modified):
                self.detectedInjectionTypes.append(comparison + " is always true")
                return True
        except:
            pass
        return False

    def check_always_false(self, query):
        query = str(query)
        and_index = query.find(" AND ")
        if and_index == -1:
            and_index = query.find(" and ")
            if and_index == -1:
                return False
        conditions = query[and_index:len(query)]
        parsed = sqlparse.parse(conditions)[0]
        comparison = str(find_next_comparison(parsed))
        if comparison == "''=''":
            self.detectedInjectionTypes.append("''='' is always true")
            return True
        comparison_modified = comparison.replace("=", "==")
        comparison_modified = comparison_modified.replace("<>", "!=")
        try:
            if not eval(comparison_modified):
                self.detectedInjectionTypes.append(comparison + " is always false")
                return True
        except:
            pass
        return False

    def check_if_blocked_keyword(self, query):
        config = configparser.ConfigParser()
        config.read('configurations.ini')
        blocked_keywords = str(config['Blocked']['blocked_keywords']).split(",")

        parsed = sqlparse.parse(query)
        for i in range(len(parsed)):
            q = parsed[i]
            blocked_keyword = find_blocked_keyword(q, blocked_keywords)
            if blocked_keyword != "":
                self.detectedInjectionTypes.append(blocked_keyword + " keyword is forbidden")
                return True
        return False

    def check_if_blocked_literal(self, query):
        config = configparser.ConfigParser()
        config.read('configurations.ini')
        blocked_literals = str(config['Blocked']['blocked_literals']).split(",")
        parsed = sqlparse.parse(query)
        for i in range(len(parsed)):
            q = parsed[i]
            blocked_literal = find_blocked_literal(q, blocked_literals)
            if blocked_literal != "":
                self.detectedInjectionTypes.append(blocked_literal + " is forbidden")
                return True
        return False

    # def check_subquery(self, query):
    #     parsed = sqlparse.parse(query)
    #     where = parsed[0][-1]
    #     comparison = str(find_next_comparison(where))
    #     if comparison.
    #
    #         if isinstance(i, sqlparse.sql.Comparison):

def find_next_comparison(parsed):
    for i in parsed.tokens:
        if isinstance(i, sqlparse.sql.Comparison):
            return i.value
        if isinstance(i, sqlparse.sql.TokenList):
            return find_next_comparison(i)

def find_blocked_keyword(parsed, blocked_keywords):
    for i in parsed.tokens:
        if i.ttype == sqlparse.tokens.Keyword.DDL and str(i.value).upper() in blocked_keywords:
            return str(i.value)
        if isinstance(i, sqlparse.sql.TokenList):
            return find_blocked_keyword(i, blocked_keywords)
    return ""

def find_blocked_literal(parsed, blocked_literals):
    for i in parsed.tokens:
        if i.ttype == sqlparse.tokens.Literal.String.Single and str(i.value) in blocked_literals:
            return str(i.value)
        if isinstance(i, sqlparse.sql.TokenList):
            blocked_literal = find_blocked_literal(i, blocked_literals)
            if blocked_literal != "":
                return blocked_literal
    return ""

def test_detector():
    detector = Detector()
    detector.isInjected("SELECT first_name, last_name, email FROM members WHERE username='admin' -- ' AND showpublic=1")
    print(detector.detectedInjectionTypes)

    detector.detectedInjectionTypes.clear()
    detector.isInjected("select col1  from table1 where col1 > 1 union select col2 from table2")
    print(detector.detectedInjectionTypes)

    detector.detectedInjectionTypes.clear()
    detector.isInjected("SELECT name, description FROM products WHERE category = 'Gifts' UNION SELECT username, password FROM users--")
    print(detector.detectedInjectionTypes)

    detector.detectedInjectionTypes.clear()
    detector.isInjected("SELECT UserId, Name, Password FROM Users WHERE UserId = 105 and (1>2);")
    print(detector.detectedInjectionTypes)

    detector.detectedInjectionTypes.clear()
    detector.isInjected("SELECT UserId, Name, Password FROM Users WHERE UserId = 105 or ''='';")
    print(detector.detectedInjectionTypes)

    # config = configparser.ConfigParser()
    # config.read('configurations.ini')
    # blocked_literals = str(config['Blocked']['blocked_literals']).split(",")
    # print(find_blocked_literal(sqlparse.parse("SELECT * FROM reviewers WHERE first_name='Mary'")[0], blocked_literals))
    #
    # parsed = sqlparse.parse("SELECT name FROM syscolumns WHERE id =(SELECT id FROM sysobjects WHERE name = 'known_table_name')")
    # parsed[0]._pprint_tree()

#test_detector()
