#!/usr/bin/python 
import os
import sys


class dbInterface:
    
    def generate4jObject(self, contact):
      ##do something
      
      obj = "create ("+contact.name.replace(" ", "_")+":contact "      
      obj += " {"
      obj += " show_name: '" + contact.show_name + "', "
      obj += "name: '"+contact.name + "', "
      obj += "email: '" + contact.email   + "', "
      obj += "address: '" + contact.address + "', "
      obj += "title: '"+contact.title + "', "
      obj += "service: '"+contact.service + "', "
      obj += "organization: '"+contact.organization + "', "
      obj += "work_number: '" + contact.work_num + "', "
      obj += "home_number: '" + contact.home_num + "', "
      obj += "cell_number: '" + contact.cell_num + "', "
      obj += "Preference: '" + contact.pref_num +"'"
      obj += "}"
      obj += ")"
      
      
      return obj, self.generateOrganizationObject(contact.service), self.generateRelationships(contact.name.replace(" ", "_"), contact.service)
      
    def generateInitial4jObject(self):
      ini = "create (Me:focal_Point {name: 'ME'})"
      return ini
      
    def generateRelationships(self, name, org):
        o = "CREATE ("+name+")-[:KNOWS]->(Me) \n"
        o += "CREATE ("+name+")-[:WORKS_IN]->("+org+")"
        return o
        
    def generateOrganizationObject(self, org):
      return "create (" + org +":service {name: '"+org+"'})"
      
    
class Contact:
  def __init__(self):
    self.type = "contact"

  def breakDownVCF(self, openVCF):            
    i = 14
    
    n = openVCF[6][2:].split(';')
    self.show_name = self.cleaner(openVCF[5][3:])
    
    self.name = n[1] + " " + n[0]  
    self.name = self.name
    
    self.email = openVCF[7][11:]
    if self.email[0:9] == "INTERNET:": self.email = self.cleaner(self.email[9:])
    if self.email == "": self.email="NONE"
    
    #8#ORG:USA;62 Med Bde
    self.service = self.cleaner(openVCF[8][4:].split(";")[0])
    self.organization = self.cleaner(openVCF[8][4:])
    
    add = openVCF[10].strip()
    add = add.replace('\n', "")
    
    if len(add) > 71: i=i+1
    add = add.split(';')

    self.address = add[3].strip() + "," + add[4].strip() + "," + add[5].strip() + "," + add[6].strip()
    if self.address.strip() == ",,,": self.address = "NONE"    
    
    title_match = [s for s in openVCF if "TITLE" in s]
    self.title = self.cleaner(title_match[0][6:])
    if self.title == "": self.title = "NONE"
    self.work_num = self.space_cleaner(self.cleaner(openVCF[i][14:]))
    if self.work_num == "": self.work_num = "NONE"
    self.home_num = self.space_cleaner(self.cleaner(openVCF[i+1][14:]))
    if self.home_num == "": self.home_num = "NONE"
    self.cell_num = self.space_cleaner(self.cleaner(openVCF[i+3][14:]))
    if self.cell_num == "":self.cell_num = "NONE"
    self.pref_num = self.space_cleaner(self.cleaner(openVCF[i+5][14:]))
    if self.pref_num == "": self.pref_num = "NONE"    
    
#    print("name: " + self.name)
#    print("title: " + self.title)
#    print("email: " + self.email)
#    print("address: " + self.address)
#    print("Work number: " + self.work_num)
#    print("Home Number: " + self.home_num)
#    print("Pref_Num: " + self.pref_num)
    return self 
    
  def cleaner(self, s):
      return s.strip().replace("\n", "").replace("\\","")
  def space_cleaner(self, s):
      return s.replace(" ", "")

    

def main():
  path = "./"
  contacts = []
  orgs = []
  db = dbInterface()  
  for subdir, dirs, files in os.walk('./'):
    for f in files:
      if os.path.splitext(path + f)[1] != ".vcf": continue
      with open(f, "r") as a:
        person = Contact()
        
        con, org, serv = db.generate4jObject(person.breakDownVCF(a.readlines()))        
        
             
        contacts.append(con)
        orgs.append(org)
        contacts.append(serv)
  
  orgs = list(set(orgs))  
  with open("contacts_output.csv", "w") as outFile:
      outFile.write(db.generateInitial4jObject() + "\n")
      for o in orgs:
          outFile.write(str(o) + "\n")
      for c in contacts:          
          outFile.write(str(c) + "\n")
          

if __name__ == "__main__":
    main()
