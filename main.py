from PyPDF2 import PdfMerger
import argparse
import os
from datetime import datetime
import pathlib
import importlib.util
import subprocess

class PDFCombinerWrapper:

    def __init__(self):
        self.checkForPDFLib()
        self.FilesToCombine=[]
        self.OutPutFileName=None
        self.PDFMerger = PdfMerger()
        self.UserCMDInput=""


    def checkForPDFLib(self):

        if not importlib.util.find_spec('PyPDF2'):
            subprocess.check_call(['pip', 'install', 'PyPDF2'])
        else:
            print("PDF Library Found. Skipping PDF Library Installation!")

    def validateFilePath(self,p):
        if os.path.exists(p):
            return True
        else:
            return False

    def handleArgs(self,args):
        #check if directory args
        if args.dir:

            #check dir
            if not self.validateFilePath(args.dir[0]):
                raise argparse.ArgumentTypeError("Directory specified cannot be found")
            else:
                # populate pdf files
                self.FilesToCombine = [str(x) for x in list(pathlib.Path(args.dir[0]).glob("*.pdf"))]

        elif args.f:
            self.FilesToCombine = args.f

        else:
            raise argparse.ArgumentTypeError("Unable to parse input values. Check and Try Again")

        self.ProcessFile()


    def main(self):

        parser = argparse.ArgumentParser()
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument("-d","--dir",type=str,required=False,nargs=1,help="Specify a directory with PDFs to combine")
        group.add_argument("-f",type=str,required=False,nargs='+',help="specify exact PDFS (and paths) to combine")

        try:
            args = parser.parse_args()
            self.handleArgs(args)
        except Exception as e:
            parser.print_help()

    def ProcessFile(self):

        for file in self.FilesToCombine:

            if self.validateFilePath(file):
                self.PDFMerger.append(file)
            else:
                print("Invalid file path ",file)

        self.OutPutFileName = os.path.join(os.getcwd(),"PDF_MERGE_"+str(datetime.now())+".pdf")
        self.PDFMerger.write(self.OutPutFileName)
        self.PDFMerger.close()
        if os.path.exists(self.OutPutFileName):print("File Successfully Created!\n")

if __name__ == '__main__':

    pdfMerger = PDFCombinerWrapper()
    pdfMerger.main()



