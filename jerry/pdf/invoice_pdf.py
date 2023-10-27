from reportlab.pdfgen import canvas
import io
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.graphics.shapes import Line, Drawing, colors
from jerry.invoice import Invoice
from jerry.company import Company
from jerry.customer import Customer
from jerry.invoice_product import InvoiceProduct


def invoicePdf(invoice: Invoice, company: Company, customer: Customer, itemList: []):

    buffer = io.BytesIO()
    invPdf = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.2*inch,
                               bottomMargin=0.1*inch, leftMargin=0.5*inch, rightMargin=0.5*inch)
    width, height = letter
    width -= 1*inch
    height -= 1*inch
    pdf = []
    # ////////////Header/////////////////
    header = [
        ["Invoice No: " + invoice.invoice_no,
            "TAX INVOICE", "Date: " + invoice.date_created],
    ]
    headerTable = Table(header, colWidths=[1/3*width, 1/3*width, 1/3*width], rowHeights=[
                        2/5*inch], spaceAfter=8, cornerRadii=[5, 5, 5, 5])
    headerTable.setStyle(TableStyle([('FONTNAME', (0, 0), (2, 0), 'Helvetica-Bold'),
                                     ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                                     ('ALIGN', (1, 0), (1, 0), 'CENTER'),
                                     ('ALIGN', (2, 0), (2, 0), 'RIGHT'),
                                     ('BOX', (0, 0), (-1, -1), 2, colors.black),
                                     ('FONTSIZE', (1, 0), (1, 0), 20),
                                     ('FONTSIZE', (0, 0), (0, 0), 12),
                                     ('FONTSIZE', (2, 0), (2, 0), 12),
                                     ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                                     ('VALIGN', (1, 0), (1, 0), 'TOP')]))
    pdf.append(headerTable)
    # ////////////Company Header///////////
    company_data = [
        [company.legal_name],
        [company.address],
        ["" + company.city + ', ' + company.state + ' - ' + company.pincode],
        ['Email-No: ' + company.email + ', Phone No: ' + company.phone_no],
        [company.website],
        ['GSTN: ' + company.gstn]]
    company_table = Table(company_data, colWidths=1*[width], rowHeights=[
                          3/8*inch, 1/4*inch, 1/4*inch, 1/4*inch, 1/4*inch, 2/5*inch], spaceAfter=8, cornerRadii=[5, 5, 5, 5])
    company_table.setStyle(TableStyle([('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
                                       ('FONTSIZE', (0, 0), (0, 0), 20),
                                       ('FONTSIZE', (0, 1), (-1, -1), 12),
                                       ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                       ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                                       ('BOX', (0, 0), (-1, -1), 2, colors.black),
                                       ('BOTTOMPADDING', (0, 5), (0, 5), 10),
                                       ]))
    pdf.append(company_table)
    # /////////////////Customer header///////////
    customer_data = [["Customer Details:",  ""],
                     ["Name           :", customer.name],
                     ["Phone No    :", customer.phone_no],
                     ["Address       :", customer.address],
                     ["", customer.state + " - " + customer.pincode]]
    customer_table = Table(customer_data, colWidths=[1/6*width, 5/6*width], rowHeights=[
        3/8*inch, 1/4*inch, 1/4*inch, 1/4*inch, 2/5*inch], spaceAfter=8, cornerRadii=[5, 5, 5, 5])
    customer_table.setStyle(TableStyle([('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
                                        ('FONTSIZE', (0, 0), (0, 0), 15),
                                        ('FONTSIZE', (0, 1), (-1, -1), 12),
                                        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                                        ('TOPPADDING', (0, 0), (0, 0), 5),
                                        ('BOX', (0, 0), (-1, -1), 2, colors.black),
                                        ('SPAN', (0, 0), (1, 0))
                                        ]))
    pdf.append(customer_table)
    # ////////////////////Product Details////////////
    productData = [["Product Details:", "", "", "", "", ""], [
        "Sl.no", "Product", "Hsn Code", "Qty", "Rate", "Amount"]]
    i = 1
    total_qty = 0
    rowHeights = [3/8*inch, 1/4*inch]
    for item in itemList:
        data = [i, Paragraph("Name: " + item.product.name + "<br/>" + "Description: " + item.invoiceProduct.description), item.product.hsn,
                item.invoiceProduct.qty, item.invoiceProduct.rate, item.invoiceProduct.qty * item.invoiceProduct.rate]
        productData.append(data)
        total_qty += item.invoiceProduct.qty
        i += 1
        rowHeights.append(3/5*inch)
    data = ["", "Total", "", total_qty, "", invoice.amount]
    productData.append(data)
    rowHeights.append(1/3*inch)
    productDataTable = Table(productData, colWidths=[width*1/16, width*7/16, width*2/16,
                             width*1/16, width*2/16, width*3/16], rowHeights=rowHeights, spaceAfter=8, cornerRadii=[5, 5, 5, 5])
    productDataTable.setStyle(TableStyle([('FONTNAME', (0, 0), (-1, 1), 'Helvetica-Bold'),
                                          ('TOPPADDING', (0, 0), (0, 0), 5),
                                          ('FONTSIZE', (0, 0), (-1, 0), 15),
                                          ('FONTNAME', (0, -1),
                                           (-1, -1), 'Helvetica-Bold'),
                                          ('FONTSIZE', (0, 1), (-1, -1), 12),
                                          ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                          ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                                          ('SPAN', (0, 0), (-1, 0)),
                                          ('INNERGRID', (0, 0),
                                           (-1, -1), 1, colors.black),
                                          ('BOX', (0, 0), (-1, -1),
                                           2, colors.black),
                                          ]))
    pdf.append(productDataTable)
    # ///////////////Paid and Due//////////////
    paymentDetail = [["Paid:", invoice.amount_paid,
                      "Due", invoice.amount - invoice.amount_paid]]
    paymentDetailTable = Table(paymentDetail, colWidths=[width*1/10, width*2/10, width*1/10, width*2/10], rowHeights=[
                               1/3*inch], hAlign='LEFT', vAlign='TOP', spaceAfter=8, cornerRadii=[5, 5, 5, 5])
    paymentDetailTable.setStyle(TableStyle([('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                                            ('FONTSIZE', (0, 0), (-1, 0), 15),
                                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                                            ('INNERGRID', (0, 0),
                                             (-1, -1), 1, colors.black),
                                            ('BOX', (0, 0), (-1, -1),
                                             2, colors.black),
                                            ]))
    # /////////Finance Detail//////////
    FinanceBody = [["Finance Details:", ""],
                   ["Financeer Name:", invoice.finance_name],
                   ["DP: ", invoice.dp],
                   ["EMI", invoice.emi],
                   ["EMI Duration:", invoice.finance_duration_in_months]]

    FinanceTable = Table(FinanceBody, colWidths=[width*2/10, width*4/10], rowHeights=[
                         3/8*inch, 1/4*inch, 1/4*inch, 1/4*inch, 1/3*inch], hAlign='LEFT', vAlign='TOP', spaceAfter=8, cornerRadii=[5, 5, 5, 5])
    FinanceTable.setStyle(TableStyle([('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
                                      ('FONTSIZE', (0, 0), (-1, 0), 15),
                                      ('FONTSIZE', (0, 1), (-1, -1), 12),
                                      ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                      ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                                      ('SPAN', (0, 0), (-1, 0)),
                                      ('INNERGRID', (0, 0),
                                       (-1, -1), 1, colors.black),
                                      ('BOX', (0, 0), (-1, -1),
                                       2, colors.black),
                                      ]))
    # ///////////////Tax Details/////
    taxDetails = [["Tax Details:", ""],
                  ["Taxable Value:", invoice.taxable_value],
                  ["CGST: ", invoice.cgst],
                  ["SGST: ", invoice.sgst],
                  ["IGST: ", invoice.igst],
                  ["Grand Total: ", invoice.amount]]

    taxDetailTable = Table(taxDetails, [width*3/18, width*4/18], rowHeights=[3/8*inch, 1/4*inch, 1/4*inch,
                           1/4*inch, 1/4*inch, 1/3*inch], hAlign='RIGHT', vAlign='TOP', spaceAfter=8, cornerRadii=[5, 5, 5, 5])
    taxDetailTable.setStyle(TableStyle([('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
                                        ('FONTSIZE', (0, 0), (-1, 0), 15),
                                        ('FONTSIZE', (0, 1), (-1, -1), 12),
                                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                                        ('SPAN', (0, 0), (-1, 0)),
                                        ('INNERGRID', (0, 0),
                                         (-1, -1), 1, colors.black),
                                        ('BOX', (0, 0), (-1, -1),
                                         2, colors.black),
                                        ]))

    t = [[paymentDetailTable, taxDetailTable], [FinanceTable, ""]]
    temp = Table(t)
    temp.setStyle(TableStyle([('SPAN', (1, 0), (1, 1))]))
    pdf.append(temp)

    # /////////Narration//////////
    narration = [["Narration:"], [Paragraph(invoice.narration)]]

    narrationTable = Table(narration, colWidths=[width*6/10], rowHeights=[
        3/8*inch, 8/11*inch], hAlign='LEFT', vAlign='TOP', cornerRadii=[5, 5, 5, 5])
    narrationTable.setStyle(TableStyle([('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
                                        ('FONTSIZE', (0, 0), (-1, 0), 15),
                                        ('FONTSIZE', (0, 1), (-1, -1), 12),
                                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                                        ('INNERGRID', (0, 0),
                                         (-1, -1), 1, colors.black),
                                        ('BOX', (0, 0), (-1, -1),
                                         2, colors.black),
                                        ]))

    # ///////////////Bank Details/////
    bankDetails = [["Bank Details:", ""],
                   ["Bank Name:", company.bank_name],
                   ["Account No: ", company.account_no],
                   ["IFSC Code: ", company.ifsc_code]]

    bankDetailTable = Table(bankDetails, [width*3/18, width*4/18], rowHeights=[3/8*inch, 1/4*inch, 1/4*inch,
                                                                               2/6*inch], hAlign='RIGHT', vAlign='TOP', cornerRadii=[5, 5, 5, 5])
    bankDetailTable.setStyle(TableStyle([('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
                                        ('FONTSIZE', (0, 0), (-1, 0), 15),
                                        ('FONTSIZE', (0, 1), (-1, -1), 12),
                                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                                        ('SPAN', (0, 0), (-1, 0)),
                                        ('INNERGRID', (0, 0),
                                         (-1, -1), 1, colors.black),
                                        ('BOX', (0, 0), (-1, -1),
                                         2, colors.black),
                                         ]))

    t = [[narrationTable, bankDetailTable]]
    temp = Table(t, spaceAfter=5)
    temp.setStyle(TableStyle())
    pdf.append(temp)
    # //////////////Footer///////
    footer = [["Reciever's Name:", "", "For " + company.legal_name], ["", "", ""], ["Signature:",
                                                          "--All Disputes are subject to " + company.city + " Jurisdiction--", "Authorised Signatory"]]

    footerTable = Table(footer, colWidths=[
                        width*5/20,width*14/27, width*5/20], cornerRadii=[5, 5, 5, 5])
    footerTable.setStyle(TableStyle([('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                     ('FONTSIZE', (0, 0), (-1, -1), 10),
                                     ('ALIGN', (0, 0), (2, 0), 'LEFT'),
                                     ('ALIGN', (-1, 0), (-1, 2), 'RIGHT'),
                                     ('FONTNAME', (1, 1), (1, 1), 'Courier'),
                                     ('ALIGN', (1, 0), (1, -1), 'CENTRE'),
                                     ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                                     ('BOX', (0, 0), (-1, -1), 2, colors.black),
                                     ]))
    pdf.append(footerTable)
    invPdf.build(pdf)
    buffer.seek(0)
    return buffer
    filename = company.name
    return FileResponse(buffer, as_attachment=True, filename=filename)
