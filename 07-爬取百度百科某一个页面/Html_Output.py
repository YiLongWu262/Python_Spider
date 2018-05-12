

class HtmlOutput(object):
    """docstring for HtmlOutput"""

    def __init__(self):
        self.datas = []

    def collect_data(self, data):
        if data is None:
            return
        self.datas.append(data)

    def output_data(self):
        index = 1
        file_out = open('output.html','w', encoding='utf-8')
        file_out.write("<html>")
        file_out.write("<body>")
        file_out.write("<table>")

        for data in self.datas:
            file_out.write("<tr>")
            file_out.write("<td>%s</td>" % index)
            file_out.write("<td>%s</td>" % data['url'])
            file_out.write("<td>%s</td>" % data['title'])
            file_out.write("<td>%s</td>" % data['summary'])
            file_out.write("</tr>")
            index = index + 1

        file_out.write("</table>")
        file_out.write("</body")
        file_out.write("</html>")
        file_out.close()