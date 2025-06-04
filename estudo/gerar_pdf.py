from weasyprint import HTML
HTML(string="<h1>Hello PDF</h1>").write_pdf("teste.pdf")

