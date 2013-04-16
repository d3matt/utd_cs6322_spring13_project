import json
import xml.dom.minidom
from xml.dom.minidom import parse, parseString

class InvalidXml(Exception):
    pass


def parse_citation(node):
    simple_element_list = [ "date",
                            "title",
                            "booktitle",
                            "pages",
                            "location",
                            "marker",
                            "journal",
                            "rawString"
                            ]
    retval = {}
    for child in node.childNodes:
        if not isinstance(child, xml.dom.minidom.Element):
            continue

        if child.nodeName in simple_element_list:
            retval[child.nodeName] = child.childNodes[0].data
        elif child.nodeName == "contexts":
            #don't know, don't care...
            pass
        elif child.nodeName == "authors":
            retval["authors"] = []
            for author in child.childNodes:
                if not isinstance(author, xml.dom.minidom.Element):
                    continue
                achild = author.childNodes[0]
                if not isinstance(achild, xml.dom.minidom.Text):
                    raise InvalidXml()
                retval["authors"].append(achild.data)
        else:
            print "\t", child.nodeName
    return retval

        
    


def parse_doc(filename):
    dom = parse(filename + ".cxml")
    citations = []
    for citation in dom.getElementsByTagName("citation"):
        attrs = citation.attributes
        if (not attrs.has_key('valid')) or (attrs.get('valid').value != 'true'):
            continue

        citations.append(parse_citation(citation))
    print json.dumps(citations, indent=2)


parse_doc("Y12-1005")
