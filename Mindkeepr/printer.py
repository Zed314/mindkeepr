from enum import Enum
import io
from reportlab.pdfgen import canvas
from reportlab.graphics import renderPDF
from reportlab.graphics.barcode import eanbc
from reportlab.graphics.shapes import Drawing
from reportlab.lib.units import mm
from reportlab.pdfbase.pdfmetrics import stringWidth

class Printer():

    def generate_centered_text(self, text, y_text, size):
        text_width = stringWidth(text[:32],"Times-Roman", size)
        textobject = self.canvas.beginText((25*mm-text_width)/2.0, y_text*mm)
        textobject.setFont('Times-Roman', size)
        textobject.textLine(text=text[:32])
        return textobject
    def generate_barcode_and_text(self, text, value, y_text):
        barcode_eanbc8 = eanbc.Ean8BarcodeWidget(value,width =22*mm, height=12*mm,barHeight=8*mm, fontSize=5)
        bounds = barcode_eanbc8.getBounds()
        width = bounds[2] - bounds[0]
        height = bounds[3] - bounds[1]
        d = Drawing(width, height)
        d.add(barcode_eanbc8)

        title = self.generate_centered_text(text,y_text,4)
        disclaimer = self.generate_centered_text("Mindkeepr",y_text-10,3)
        return d, title, disclaimer
    def print_to_canvas(self,element, element2):
        barcode, title, disclaimer  = self.generate_barcode_and_text(element.name, element.id, 24)
        self.canvas.drawText(title)
        self.canvas.drawText(disclaimer)
        renderPDF.draw(barcode,self.canvas,-1.5*mm, 15*mm)
        barcode, title, disclaimer  = self.generate_barcode_and_text(element2.name, element2.id, 11)
        self.canvas.drawText(title)
        self.canvas.drawText(disclaimer)
        renderPDF.draw(barcode,self.canvas,-1.5*mm, 2*mm)
        self.canvas.showPage()
    def __init__(self):
        self.printlist = {}
        self.buffer = io.BytesIO()
        #self.canvas = canvas.Canvas("form.pdf",pagesize=(1000,1000))#pagesize=(25,26))
        self.canvas = canvas.Canvas(self.buffer,pagesize=(25*mm,26*mm))
        #for i in range(0,10):
        #    self.print_to_canvas(Elt(i*13,"ee"),Elt(i*12,"ee"))
        #self.canvas.save()


    def add_element_to_print_list(self, element,qty=1):
        tuple = self.printlist.get(element.id)
        if (tuple):
            tuple[1]=tuple[1]+qty
        else:
            self.printlist[element.id]=[element,qty]
    def set_qty_element_print_list(self,element,qty):
        if qty == 0:
            self.printlist.pop(element.id,None)
            return
        tuple = self.printlist.get(element.id)
        if (tuple):
            tuple[1]=qty
        else:
            self.printlist[element.id]=[element,qty]
    def get_qty_element_print_list(self,element):
        tuple = self.printlist.get(element.id)
        if (tuple):
            return tuple[1]
        else:
            return 0
    def get_print_list(self):
        return list(self.printlist.values())
    def render_print_list(self):
        # rendering
        #for work in self.printlist.values():
        #    self._create_barcode(work[0].id,work[0].name)
        current_elements = []
        pos_max = 2

        for i in range(len(self.printlist.values())):
            for occ in range(list(self.printlist.values())[i][1]):
                current_elements.append(list(self.printlist.values())[i][0])
                if len(current_elements) == pos_max:
                    self.print_to_canvas(current_elements[0],current_elements[1])
                    current_elements.clear()

        if(len(current_elements)!=0):
            for i in range(pos_max-len(current_elements)):
                current_elements.append(current_elements[-1])
            self.print_to_canvas(current_elements[0],current_elements[1])
        #pb in second printk
        self.canvas.save()
        return self.buffer.getvalue()