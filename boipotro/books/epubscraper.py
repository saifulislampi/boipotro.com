#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import subprocess
import xmltodict
from re import sub, search
import json
from zipfile import ZipFile
from PIL import Image
from multiprocessing import Pool
from functools import partial
from time import time
from itertools import groupby
"""
Book subject and types data
"""
typel = ["উপন্যাস", "বড়গল্প", "ছোটগল্প", "কবিতা", "প্রবন্ধ", "নাটক", "গান", "সমগ্র"]

subl = {"Absurd": "স্বপ্নবাস্তবতা", "Action": "দুঃসাহসিক", "Adventure": "দুঃসাহসিক", "Autobiography": "আত্নজীবনী", "Biography": "জীবনী", "Children's literature": "শিশুসাহিত্য", "Classic": "চিরায়ত সাহিত্য", "Collection": "সমগ্র", "Comedy": "রম্যরচনা", "Crime": "অপরাধ", "Detective": "গোয়েন্দা", "Drama": "নাটক", "Epic": "মহাকাব্য", "Essay": "প্রবন্ধ", "Fable": "রূপকথা", "Fairy tale": "রূপকথা", "Fanciful": "স্বপ্নবাস্তবতা", "Fantasy": "রূপকথা", "Folklore": "লোকসাহিত্য", "Historical fiction": "ঐতিহাসিক উপন্যাস", "History": "ইতিহাস", "Horror": "ভৌতিক", "Humour": "রস", "Legend": "উপ্যাখান", "Magical realism": "জাদুবাস্তবতা", "Memoir": "স্মৃতিচারণ", "Mystery": "রহস্য", "Mythology": "পুরাণ", "Novel": "উপন্যাস", "Novella": "বড়গল্প", "Philosophy": "দর্শন", "Play": "নাটক", "Poem": "কবিতা", "Politics": "রাজনীতি", "Realistic fiction": "বাস্তবিক", "Religion": "ধর্ম", "Romance": "প্রেম", "Satire": "ব্যাঙ্গরচনা", "Science": "বিজ্ঞান", "Science fiction": "কল্পবিজ্ঞান", "Song": "গান", "Speech": "ভাষণ", "Story": "ছোটগল্প", "Short story": "ছোটগল্প", "Surreal": "স্বপ্নবাস্তবতা", "Travel": "ভ্রমণকাহিনী", "Dance-drama": "নৃত্যনাট্য"}

def namef (string):
    return string.split('/')[-1]

def imscrap (booklink, imagedir, imagename, imagelink, overwrite):
    """
    Scrap Cover image from epub.
    """
    imagename+="."+namef(imagelink).split('.')[-1]

    target = os.path.join(imagedir, imagename)
    if overwrite == True:
        try:
            os.remove(target)
        except:
            pass
    if os.path.isfile(target) == True:
        return target
    else:
        with ZipFile(booklink) as book:
            with book.open(imagelink) as cover:
                img = Image.open(cover)
                img = img.resize((225*2, 318*2), Image.ANTIALIAS)
                img.save(target)
        return target


def link_parser(dstring):
    """
    Github repository link perser
    """
    data = dstring.split('(http')
    if len(data) == 2:
        return data[0].strip()
    else:
        return data[0].strip()

def book_keeper (booklink):
    """
    Book cataloger based on metadata
    """
    with ZipFile(booklink) as book:
        with book.open('OEBPS/content.opf') as cont:
            data = xmltodict.parse(cont.read())['package']
    meta = data['metadata']
    version = data['@version'][0]
    catalog = {'author': [], 'publisher': [], 'translator': [], 'editor': [], 'illustrator': [], 'subject': []}
    for key, val in meta.items():
        if key == 'dc:title':
            catalog['title'] = val
        elif key == 'dc:creator':
            if version == '2':
                if isinstance(val, list):
                    for v in val:
                        if v['@opf:role'] == 'aut':
                            catalog['author'].append(link_parser(v['#text']))
                else:
                    if val['@opf:role'] == 'aut':
                        catalog['author'].append(link_parser(val['#text']))
            elif version == '3':
                if isinstance(val, list):
                    metas = {}
                    for m in meta['meta']:
                        try:
                            if m['#text'] in ['aut', 'ill', 'edt', 'trl', 'pbl']:
                                if m['@refines'][0] == "#":
                                    res = m['@refines'][1:]
                                else:
                                    res = m['@refines']
                                metas[res] = m['#text']
                        except:
                            pass
                    vals = {}
                    for v in val:
                        if v['@id'][0] == "#":
                            res = v['@id'][1:]
                        else:
                            res = v['@id']
                        vals[res] = v['#text']
                    for k, v in metas.items():
                        if v == 'aut':
                            catalog['author'].append(link_parser(vals[k]))
                        elif v == 'trl':
                            catalog['translator'].append(link_parser(vals[k]))
                        elif v == 'edt':
                            catalog['editor'].append(link_parser(vals[k]))
                        elif v == 'ill':
                            catalog['illustrator'].append(link_parser(vals[k]))
                        elif v == 'pbl':
                            catalog['publisher'].append(link_parser(vals[k]))
                else:
                    metas = {}
                    for m in meta['meta']:
                        try:
                            if m['#text'] in ['aut', 'ill', 'edt', 'trl', 'pbl']:
                                if m['@refines'][0] == "#":
                                    res = m['@refines'][1:]
                                else:
                                    res = m['@refines']
                                metas[res] = m['#text']
                        except:
                            pass
                    vals = {}
                    if val['@id'][0] == "#":
                        res = val['@id'][1:]
                    else:
                        res = val['@id']
                    vals[res] = val['#text']
                    for k, v in metas.items():
                        if v == 'aut':
                            catalog['author'].append(link_parser(vals[k]))
                        elif v == 'trl':
                            catalog['translator'].append(link_parser(vals[k]))
                        elif v == 'edt':
                            catalog['editor'].append(link_parser(vals[k]))
                        elif v == 'ill':
                            catalog['illustrator'].append(link_parser(vals[k]))
                        elif v == 'pbl':
                            catalog['publisher'].append(link_parser(vals[k]))
        elif key == 'dc:language':
            catalog['language'] = val
        elif key == 'dc:description':
            catalog['description'] = val
        elif key == 'dc:publisher':
            if isinstance(val, list):
                for v in val:
                    catalog['publisher'].append(link_parser(v))
            else:
                catalog['publisher'].append(link_parser(val))
        elif key == 'dc:type' or key == 'dc:subject':


            try:
                if isinstance(val, list):
                    for v in val:
                        catalog['subject'].append(subl[v.capitalize()])
                else:
                    catalog['subject'].append(subl[val.capitalize()])
            except:
                pass
        elif key == 'dc:contributor':
            if isinstance(val, list):
                for v in val:
                    role = v['@opf:role']
                    if role == 'trl':
                        catalog['translator'].append(link_parser(v['#text']))
                    elif role == 'edt':
                        catalog['editor'].append(link_parser(v['#text']))
                    elif role == 'ill':
                        catalog['illustrator'].append(link_parser(v['#text']))
            else:
                role = val['@opf:role']
                if role == 'trl':
                    catalog['translator'].append(link_parser(val['#text']))
                elif role == 'edt':
                    catalog['editor'].append(link_parser(val['#text']))
                elif role == 'ill':
                    catalog['illustrator'].append(link_parser(val['#text']))
        elif key == 'dc:date':
            if version == '3':
                catalog['pubdate'] = val
            else:
                if isinstance(val, list):
                    for v in val:
                        event = v['@opf:event']
                        if event == 'publication' or event == 'creation':
                            catalog['pubdate'] = v['#text']
                        elif event == 'modification':
                            catalog['moddate'] = v['#text']
                else:
                    try:
                        event = val['@opf:event']
                        if event == 'publication' or event == 'creation':
                            catalog['pubdate'] = val['#text']
                        elif event == 'modification':
                            catalog['moddate'] = val['#text']
                    except:
                        try:
                            catalog['pubdate'] = val
                        except:
                            pass
        elif key == 'meta':
            for v in val:
                try:
                    if v['@name'] == 'cover':
                        catalog['cover'] = "OEBPS/Images/" + v['@content']
                except:
                    try:
                        if v['@property'] == 'dcterms:modified':
                            catalog['moddate'] = v['#text'][:10]
                    except:
                        pass
    subject = catalog['subject']
    precount = len(subject)
    for s in subject:
        if s in typel:
            catalog['type'] = s
            catalog['subject'].remove(s)
    if len(catalog['subject']) == precount:
        catalog['type'] = 'অন্যান্য'
    return catalog
