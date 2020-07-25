from Java8Lexer import Java8Lexer
from Java8ParserListener import Java8ParserListener
from Java8Parser import Java8Parser
import graphviz
import antlr4
import sys

count = 0

def mywalk(expr, graph, rules):
    global count

    if (isinstance(expr, antlr4.tree.Tree.TerminalNode)):
        graph.node(name = str(count), label = expr.getText())
        node = str(count)
        count += 1
        return node

    childno = expr.getChildCount()
    t =  expr.getRuleIndex()

    if childno == 1:
        for j in expr.getChildren():
            if(isinstance(j, antlr4.tree.Tree.TerminalNode)):
                node = str(count)
                graph.node(name = node, label = expr.getText() + ' (' + rules[t] + ')')
                count += 1
            else:    
                node = mywalk(j, graph, rules)
            return node

    node = str(count)
    graph.node(name = node, label = rules[t])

    count += 1
    for i in expr.getChildren():
        nodec = mywalk(i, graph, rules)
        graph.edge(node, nodec)

    return node


def main():
    lexer = Java8Lexer(antlr4.StdinStream())
    stream = antlr4.CommonTokenStream(lexer)
    parser = Java8Parser(stream)
    rules = parser.ruleNames
    tree = parser.compilationUnit()
    graph = graphviz.Digraph(format='dot')
    mywalk(tree, graph, rules)

    # graph.write(sys.argv[1], format='dot')
    # graph.write_png('example2.png')

    graph.render(sys.argv[1])

if __name__ == '__main__':
    main()