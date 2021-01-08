#!/usr/bin/python
# coding=<utf-8>

"""
Find_span: program to find span (made by yourself) into a multilingual text.
Autor: Pilar Hidalgo
Github: https://github.com/PilarHidalgo

Usage:
    from Find_SPAN import Find_SPAN as fs
    finder_r=fs.SpanFinder('Dictionary.xlsx','Sheet','excel')
    finder_r.find_span('i love Dog’s tooth in pants','tuple')

 Given a text (input_data) and a dictionary created especially to identify SPAN's, related terms or words, 
 this little program can extract terms in three formats: tuple (e.g ('label','term/list of terms')),just the term/terms or just the
 label of the SPAN. 

Further details are in the comments within the code.

Input format for diccionary:

example IN EXCEL AND JSON dictionary: https://drive.google.com/drive/folders/1MdNpN3RtLoAn98QukWqerV2Guo_K9G_o?usp=sharing

also can use this format:
#Clothes and garmends related terms examples
(i)
    [
        [
            {'label':'SPAN1_NAME','pattern':'word/terms'},
            {'label':'SPAN2_NAME','pattern':'word/terms'},
            ...
            {'label':'SPANn_NAME','pattern':'word/terms'}
            #EXAMPLES
            #{'label':'Material', 'pattern': 'alpaca'},
            #{'label':'Body_shape','pattern': 'fanny'},
            #{'label':'Pattern', 'pattern': 'Checkered Patterns'},
            #{'label':'Style', 'pattern': 'vintage'}
        ]
    ]

Output formats of Find_span:
(i) Tuple:
    [('label','text')]
(ii) Just_label
    'label' #string type
(iii) Just_text
    'text' #string type
"""

import sys
sys.path.append("..")
from itertools import chain
import more_itertools as mit

import pandas as pd
import spacy
from spacy.lang.xx import MultiLanguage
from spacy.pipeline import EntityRuler
from tqdm import tqdm, trange
import os
import re

#GET THE PARAMETERS FOR Find_span
#Type_file_dict=type_file#/'json','excel', 'csv' or None if you are using format mention in (i) into the Usage explanation
#diccionary_o=file_dictionary#'file_dictionary' or name variable of your diccionary (type)
#output_format=op_format #('tuple','just_terms','just_label')


#FIND SPAN FUNCTION
class SpanFinder:
    def __init__(self,io,sheetname,Type_file_dict):
        self.io = io        
        self.Type_file_dict= Type_file_dict
        self.sheetname = sheetname
        #self.op_format = op_format
        self.df= self.read_data()
        self.patterns = self.read_patterns()
        self.nlp = self.set_nlp()
        self.trans = self.make_trans()
    #FIND SPAN FUNCTION
    def read_data(self):
        if self.Type_file_dict=='json':
            df=pd.read_json(self.io)
        elif self.Type_file_dict=='excel':
            df=pd.read_excel(self.io,sheet_name=self.sheetname)
        elif self.Type_file_dict=='csv':
            df=pd.read_csv(self.io)
        #df
        return df

    def read_patterns(self):#,Type_file_dict):
        a=self.df
        #carga el diccionario por label
        for k in range(2,len(a.columns)-1):
                exec(f'a{k} = a[["label","pattern.{k}"]]')
                #rename las columnas
        sheets=[]    
        for var in dir():
            if isinstance(locals()[var], pd.core.frame.DataFrame)  and var[0]!='_':
                sheets.append(var)
        df_list=[]
        for i in range(1,len(sheets)): 
            df_list.append(eval(sheets[i]))        

            #rename patterns columns
        for k in range(0,len(df_list)):#(len(df.columns)-2)):
            df_list[k]=df_list[k].rename(columns={df_list[k].columns[1]:"pattern"}, inplace = False)
            #diccionario
        for k in range(0,len(df_list)):
            exec(f'patterns{k+1} = df_list[k].to_dict(orient="records")')
        patt_list=[]    
        for var in dir():
            if var.startswith('patterns')==True and var[0]!='_':
                patt_list.append(eval(var))
        patterns=[]
        for i in range(0,len(patt_list)):
            patterns= patterns+patt_list[i]   
        return patterns
    
    def set_nlp(self):
        #Crear el objeto NLP
        nlp = MultiLanguage()
        ruler = EntityRuler(nlp)
        ruler.add_patterns(self.patterns)
        nlp.add_pipe(ruler)
        return nlp
    
    def make_trans(self):
        #Preprocesar la entrada
        a,b = 'áéíóúü','aeiouu'
        trans = str.maketrans(a,b)
        return trans
    
    def find_span(self, sentence,op_format):
        #sentence=sentence.lower().translate(self.trans)
        #doc = self.nlp(sentence)
        #Devuelve la etiqueta real de la entidad
        if op_format=='tuple':
            sentence=sentence.lower().translate(self.trans)
            doc = self.nlp(sentence)
                #Returns the actual label of the entity
            if (sentence=='' or  sentence==' ' or sentence=='NaN'):
                output=['No found']
            else: 
                output= list(set([(ent.label_,ent.text) for ent in doc.ents]))
                #element no found
            if output!=[]:
                output=output
            else: output=['No found']
            return output[0]
    
        if op_format=='text':
            sentence=sentence.lower().translate(self.trans)
            doc = self.nlp(sentence)
                #Returns the actual label of the entity
            if (sentence=='' or  sentence==' ' or sentence=='NaN'):
                output=['No found']
            else: 
                output= list(set([(ent.text) for ent in doc.ents]))
                #element no found
            if output!=[]:
                output=output
            else: output=['No found']
            return output[0]
        if op_format=='label':
            sentence=sentence.lower().translate(self.trans)
            doc = self.nlp(sentence)
                #Returns the actual label of the entity
            if (sentence=='' or  sentence==' ' or sentence=='NaN'):
                output=['No found']
            else: 
                output= list(set([(ent.label_) for ent in doc.ents]))
                #element no found
            if output!=[]:
                output=output
            else: output=['No found']
            return output[0] 
