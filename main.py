from tkinter import *
from tkinter import ttk
import sqlite3

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Image
import webbrowser


janela = Tk()


class Relatorios:
  def printProcesso(self):
    webbrowser.open('processo.pdf')

  def gerarRelatProcesso(self):
    self.c = canvas.Canvas('processo.pdf')
    self.codigoRel = self.entry_codigo.get()
    self.processoRel = self.entry_processo.get()
    self.empresaRel = self.entry_empresa.get()
    self.empRel = self.entry_emp.get()
    self.certidaoRel = self.entry_certidao.get()
    self.ataRel = self.entry_ata.get()
    self.notaRel = self.entry_nota_fiscal.get()    
    self.liquidacaoRel = self.entry_liquidacao.get()
    self.gestorRel = self.entry_gestor.get()
    self.fiscalRel = self.entry_fiscal.get()
    self.irRel = self.entry_ir.get()
    self.simplesRel = self.entry_simples.get()
    self.pendenciasRel = self.entry_pendencias.get('1.0',END)

    self.c.setFont('Helvetica-Bold', 24)
    self.c.drawString(200, 790, 'Processo: ' + self.processoRel)

    self.c.setFont('Helvetica-Bold', 18)
    self.c.drawString(50, 760, 'Empresa: ')
    self.c.drawString(50, 730, 'Emp: ')
    self.c.drawString(50, 700, 'Certidão: ')
    self.c.drawString(50, 670, 'ATA: ')
    self.c.drawString(50, 640, 'Nota Fiscal: ')
    self.c.drawString(50, 610, 'Liquidação: ')
    self.c.drawString(50, 580, 'Gestor: ')
    self.c.drawString(50, 550, 'Fiscal: ')
    self.c.drawString(50, 520, 'IR: ')
    self.c.drawString(50, 490, 'Simples: ')
    self.c.drawString(50, 460, 'Pendências: ')

    self.c.setFont('Helvetica', 18)
    self.c.drawString(170, 760, self.empresaRel)
    self.c.drawString(170, 730, self.empRel)
    self.c.drawString(170, 700, self.certidaoRel)
    self.c.drawString(170, 670, self.ataRel)
    self.c.drawString(170, 640, self.notaRel)
    self.c.drawString(170, 610, self.liquidacaoRel)
    self.c.drawString(170, 580, self.gestorRel)
    self.c.drawString(170, 550, self.fiscalRel)
    self.c.drawString(170, 520, self.irRel)
    self.c.drawString(170, 490, self.simplesRel)
    self.c.drawString(170, 460, self.pendenciasRel)
    
    

    self.c.showPage()
    self.c.save()
    self.printProcesso()
    
    
    

class Funcs:
  def limpa_tela(self):
    self.entry_codigo.delete(0, END)
    self.entry_processo.delete(0, END)
    self.entry_empresa.delete(0, END)
    self.entry_emp.delete(0, END)
    self.entry_certidao.delete(0, END)
    self.entry_ata.delete(0, END)
    self.entry_nota_fiscal.delete(0, END)
    self.entry_empresa.delete(0, END)
    self.entry_liquidacao.delete(0, END)
    self.entry_gestor.delete(0, END)
    self.entry_fiscal.delete(0, END)
    self.entry_ir.delete(0, END)
    self.entry_simples.delete(0, END)
    self.entry_pendencias.delete('1.0', END)

  def conectar_bd(self):
    self.conn = sqlite3.connect("processos.db")
    self.cursor = self.conn.cursor()
    print("Conectado ao banco de dados.")

  def desconectar_bd(self):
    self.conn.close()
    print("Desconectado do banco de dados.")

  def monta_tabelas(self):
    self.conectar_bd()
    self.cursor.execute("""
    CREATE TABLE IF NOT EXISTS processos (
        codigo INTEGER PRIMARY KEY AUTOINCREMENT,
        processo TEXT,
        empresa TEXT,
        emp TEXT,
        certidao TEXT,
        ata TEXT,
        nota_fiscal TEXT,        
        liquidacao TEXT,
        gestor TEXT,
        fiscal TEXT,
        ir TEXT,
        simples TEXT,
        pendencias TEXT
    )
    """)
    self.conn.commit()
    self.desconectar_bd()
  def variaveis(self):
    self.entry_processo.get()
    self.entry_empresa.get()
    self.entry_emp.get()
    self.entry_certidao.get()
    self.entry_ata.get()
    self.entry_nota_fiscal.get()
    self.entry_liquidacao.get()
    self.entry_gestor.get()
    self.entry_fiscal.get()
    self.entry_ir.get()
    self.entry_simples.get()
    self.entry_pendencias.get('1.0',END)
    

  def add_processo(self):
    self.conectar_bd()
    self.cursor.execute("""
    INSERT INTO processos (processo, empresa, emp, certidao, ata, nota_fiscal, liquidacao, gestor, fiscal, ir, simples, pendencias)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (self.entry_processo.get(), self.entry_empresa.get(), self.entry_emp.get(), self.entry_certidao.get(), self.entry_ata.get(), self.entry_nota_fiscal.get(), self.entry_liquidacao.get(), self.entry_gestor.get(), self.entry_fiscal.get(), self.entry_ir.get(), self.entry_simples.get(), self.entry_pendencias.get('1.0',END)))
    self.conn.commit()
    self.desconectar_bd()
    self.select_all()
    self.limpa_tela()

  def select_all(self):
    self.listaPro.delete(*self.listaPro.get_children())
    self.conectar_bd()
    lista = self.cursor.execute("""
    SELECT codigo, processo, empresa, emp, certidao, ata, nota_fiscal, liquidacao, gestor, fiscal, ir, simples, pendencias FROM processos
    """)
    for i in lista:
      self.listaPro.insert("", END, values=i)
    self.desconectar_bd()

  def buscar(self):
    self.conectar_bd()
    self.listaPro.delete(*self.listaPro.get_children())
    self.cursor.execute("""
    SELECT codigo, processo, empresa, emp, certidao, ata, nota_fiscal, liquidacao, gestor, fiscal, ir, simples, pendencias FROM processos WHERE processo = ?
    """, (self.entry_processo.get(),))
    for i in self.cursor:
      self.listaPro.insert("", END, values=i)
    self.limpa_tela()
    self.desconectar_bd()

  def duplo_clique(self, event):
    self.limpa_tela()
    self.listaPro.selection()
    for i in self.listaPro.selection():
      self.listaPro.item(i)
      self.entry_codigo.insert(END, self.listaPro.item(i)['values'][0])
      self.entry_processo.insert(END, self.listaPro.item(i)['values'][1])
      self.entry_empresa.insert(END, self.listaPro.item(i)['values'][2])
      self.entry_emp.insert(END, self.listaPro.item(i)['values'][3])
      self.entry_certidao.insert(END, self.listaPro.item(i)['values'][4])
      self.entry_ata.insert(END, self.listaPro.item(i)['values'][5])
      self.entry_nota_fiscal.insert(END, self.listaPro.item(i)['values'][6])
      self.entry_liquidacao.insert(END, self.listaPro.item(i)['values'][7])
      self.entry_gestor.insert(END, self.listaPro.item(i)['values'][8])
      self.entry_fiscal.insert(END, self.listaPro.item(i)['values'][9])
      self.entry_ir.insert(END, self.listaPro.item(i)['values'][10])
      self.entry_simples.insert(END, self.listaPro.item(i)['values'][11])
      self.entry_pendencias.insert(END, self.listaPro.item(i)['values'][12])
      
      

  def deletar_processo(self):
    self.variaveis()
    self.conectar_bd()
    self.cursor.execute("""
    DELETE FROM processos WHERE codigo = ?
    """, (self.entry_codigo.get(),))
    self.conn.commit()
    self.desconectar_bd()
    self.limpa_tela()
    self.select_all()

  def atualizar_processo(self):
    self.variaveis()
    self.conectar_bd()
    self.cursor.execute(""" UPDATE processos SET processo = ?, empresa = ?, emp = ?, certidao = ?, ata = ?, nota_fiscal = ?, liquidacao = ?, gestor = ?, fiscal = ?, ir = ?, simples = ?, pendencias = ? WHERE codigo = ?""",  (self.entry_processo.get(), self.entry_empresa.get(), self.entry_emp.get(), self.entry_certidao.get(), self.entry_ata.get(), self.entry_nota_fiscal.get(), self.entry_liquidacao.get(), self.entry_gestor.get(), self.entry_fiscal.get(), self.entry_ir.get(), self.entry_simples.get(), self.entry_pendencias.get('1.0',END), self.entry_codigo.get()))
    self.conn.commit()
    self.desconectar_bd()
    self.select_all()
    self.limpa_tela()    
    
    
class Processos(Funcs, Relatorios):
  def __init__(self):
    self.janela = janela
    self.config_janela()
    self.criar_botoes()
    self.label_tela()
    self.lista_processos()
    self.monta_tabelas()
    self.select_all()
    self.menus()

    janela.mainloop()

  def config_janela(self):
    self.janela.title('Conferência de Processos')
    self.janela.geometry('700x600')    

  def criar_botoes(self):
    self.botao_cadastrar = Button(self.janela, text='Cadastrar', command=self.add_processo)
    self.botao_cadastrar.place(relx=0.15, rely=0.015, relheight=0.07)
    self.botao_listar = Button(self.janela, text='Limpar', command=self.limpa_tela)
    self.botao_listar.place(relx=0.35, rely=0.015, relheight=0.07)
    self.botao_pesquisar = Button(self.janela, text='Buscar', command=self.buscar)
    self.botao_pesquisar.place(relx=0.50, rely=0.015, relheight=0.07)
    self.botao_editar = Button(self.janela, text='Editar', command=self.atualizar_processo)
    self.botao_editar.place(relx=0.65, rely=0.015, relheight=0.07)
    self.botao_excluir = Button(self.janela, text='Excluir', command=self.deletar_processo)
    self.botao_excluir.place(relx=0.80, rely=0.015, relheight=0.07)

  def label_tela(self):
    self.label_codigo = Label(self.janela, text='Código', font=('Arial', 10), fg='black')
    self.label_codigo.place(relx=0.01, rely=0.01)
    self.entry_codigo = Entry(self.janela, width=10)
    self.entry_codigo.place(relx=0.01, rely=0.05)

    self.label_processo = Label(self.janela, text='PROCESSO:', font=('Arial', 10, 'bold'), fg='black')
    self.label_processo.place(relx=0.01, rely=0.10)
    self.entry_processo = Entry(self.janela)
    self.entry_processo.place(relx=0.01, rely=0.15, relwidth=0.22)

    self.label_empresa = Label(self.janela, text='EMPRESA:', font=('Arial', 10, 'bold'))
    self.label_empresa.place(relx=0.25, rely=0.10)
    self.entry_empresa = Entry(self.janela)
    self.entry_empresa.place(relx=0.25, rely=0.15, relwidth=0.22)

    self.label_emp = Label(self.janela, text='EMP.:', font=('Arial', 10, 'bold'))
    self.label_emp.place(relx=0.49, rely=0.10)
    self.entry_emp = Entry(self.janela)
    self.entry_emp.place(relx=0.49, rely=0.15, relwidth=0.22)

    self.label_certidao = Label(self.janela, text='CERTIDÕES:', font=('Arial', 10, 'bold'))
    self.label_certidao.place(relx=0.73, rely=0.10)
    self.entry_certidao = Entry(self.janela)
    self.entry_certidao.place(relx=0.73, rely=0.15, relwidth=0.25)

    self.label_ata = Label(self.janela, text='ATA/CONT:', font=('Arial', 10, 'bold'))
    self.label_ata.place(relx=0.01, rely=0.20)
    self.entry_ata = Entry(self.janela)
    self.entry_ata.place(relx=0.01, rely=0.25, relwidth=0.22)

    self.label_nota_fiscal = Label(self.janela, text='NOTA FISCAL:', font=('Arial', 10, 'bold'))
    self.label_nota_fiscal.place(relx=0.25, rely=0.20)
    self.entry_nota_fiscal = Entry(self.janela)
    self.entry_nota_fiscal.place(relx=0.25, rely=0.25, relwidth=0.22)

    self.label_liquidacao = Label(self.janela, text='LIQUIDAÇÃO:', font=('Arial', 10, 'bold'))
    self.label_liquidacao.place(relx=0.49, rely=0.20)
    self.entry_liquidacao = Entry(self.janela)
    self.entry_liquidacao.place(relx=0.49, rely=0.25, relwidth=0.22)

    self.label_gestor = Label(self.janela, text='GESTOR:', font=('Arial', 10, 'bold'))
    self.label_gestor.place(relx=0.73, rely=0.20)
    self.entry_gestor = Entry(self.janela)
    self.entry_gestor.place(relx=0.73, rely=0.25, relwidth=0.25)

    self.label_fiscal = Label(self.janela, text='FISCAL:', font=('Arial', 10, 'bold'))
    self.label_fiscal.place(relx=0.01, rely=0.30)
    self.entry_fiscal = Entry(self.janela)
    self.entry_fiscal.place(relx=0.01, rely=0.35, relwidth=0.22)

    self.label_ir = Label(self.janela, text='IR:', font=('Ariel', 10, 'bold'))
    self.label_ir.place(relx=0.25, rely=0.30)
    self.entry_ir = Entry(self.janela)
    self.entry_ir.place(relx=0.25, rely=0.35, relwidth=0.22)

    self.label_simples = Label(self.janela, text='SIMPLES:', font=('Ariel', 10, 'bold'))
    self.label_simples.place(relx=0.49, rely=0.30)
    self.entry_simples = Entry(self.janela)
    self.entry_simples.place(relx=0.49, rely=0.35, relwidth=0.22)

    self.label_pendencias = Label(self.janela, text='PENDÊNCIAS/OBSERVAÇÕES:', font=('Ariel', 10, 'bold'))
    self.label_pendencias.place(relx=0.01, rely=0.40)
    self.entry_pendencias = Text(self.janela)
    self.entry_pendencias.place(relx=0.01, rely=0.45, relwidth=0.70, height=50)

  def lista_processos(self):
    self.listaPro = ttk.Treeview(self.janela, height=2, columns=('c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'c10', 'c11', 'c12', 'c13'))
    self.listaPro.heading('#0', text='')
    self.listaPro.heading('#1', text='Cód.')
    self.listaPro.heading('#2', text='Processo')
    self.listaPro.heading('#3', text='Empresa')
    self.listaPro.heading('#4', text='Emp')
    self.listaPro.heading('#5', text='Certidão')
    self.listaPro.heading('#6', text='ATA')
    self.listaPro.heading('#7', text='Nota Fiscal')
    self.listaPro.heading('#8', text='Liquidação')
    self.listaPro.heading('#9', text='Gestor')
    self.listaPro.heading('#10', text='Fiscal')
    self.listaPro.heading('#11', text='IR')
    self.listaPro.heading('#12', text='Simples')
    self.listaPro.heading('#13', text='Pendências')  
    

    self.listaPro.column('#0', width=0)
    self.listaPro.column('#1', width=50)
    self.listaPro.column('#2', width=100)
    self.listaPro.column('#3', width=100)
    self.listaPro.column('#5', width=100)
    self.listaPro.column('#6', width=100)
    self.listaPro.column('#7', width=100)
    self.listaPro.column('#8', width=100)
    self.listaPro.column('#9', width=100)
    self.listaPro.column('#10', width=100)
    self.listaPro.column('#11', width=100)
    self.listaPro.column('#12', width=100)
    self.listaPro.column('#13', width=100)    
    
    self.listaPro.place(relx=0.01, rely=0.55, relwidth=0.95, relheight=0.40)

    self.scroolLista = Scrollbar(self.janela, orient='vertical')
    self.scroolListaH = Scrollbar(self.janela, orient='horizontal')
    self.listaPro.configure(yscrollcommand=self.scroolLista.set)
    self.scroolLista.place(relx=0.96, rely=0.55, relwidth=0.03, relheight=0.43)
    self.listaPro.configure(xscrollcommand=self.scroolListaH.set)
    self.scroolListaH.configure(command=self.listaPro.xview)
    self.scroolListaH.place(relx=0.01, rely=0.95, relwidth=0.95, relheight=0.03)
    self.listaPro.bind('<Double-1>', self.duplo_clique)

  def menus(self):
      menubar = Menu(self.janela)
      self.janela.config(menu=menubar)
      filemenu = Menu(menubar)
      filemenu2 = Menu(menubar)

      def quit():
          self.janela.destroy()

      menubar.add_cascade(label='Opções', menu=filemenu)
      menubar.add_cascade(label='Relatórios', menu=filemenu2)
    
      filemenu.add_command(label='Sair', command=quit)
      filemenu.add_command(label='Limpar tela', command=self.limpa_tela)

      filemenu2.add_command(label='Informações processo', command=self.gerarRelatProcesso)  # Adicione sua funcionalidade aqui
    
    

Processos()
    

    
    