from __future__ import division
import ROOT
class CmsDecoration(object):
    def __init__(self, extraText=None, additionalText=None, lumiText="19.7 fb^{-1} (8 TeV)", align="left", valign="top", vspace=0, hspace=0, referenceHeight=None, pad=None):
        self.cmsTextFont          = 61   # Fonts
        self.lumiTextFont         = 42
        self.extraTextFont        = 52
        self.additionalTextFont   = 42
        self.cmsTextSize          = 0.9  #Text sizes
        self.lumiTextSize         = 0.6
        self.extraTextSize        = 0.76*self.cmsTextSize
        self.additionalTextSize   = 1.0*self.extraTextSize
        self.additionalTextVspace = 0.3*self.extraTextSize
        self.lumiTextOffset       = 0.2
        self.extraTextOffset      = 2.5  # only used in outOfFrame version
        #self.referenceSize        = 0.1
        self.relPosX    = 0.055  #relative padding
        self.relPosY    = 0.035#55
        self.relExtraDY = 1.3    #line height
        self.extraText, self.additionalText, self.lumiText = extraText, additionalText, lumiText
        self.align, self.valign, self.vspace, self.hspace = align, valign, vspace, hspace
        
        if pad:
            self.pad=pad
        else:
            for i in range(1000):
                self.pad = ROOT.gROOT.GetSelectedPad()
                print "mark",self.pad
                if repr(self.pad)!="<ROOT.TVirtualPad object at 0x(nil)>": break
        if referenceHeight:
            self.referenceHeight = referenceHeight
        else:
            self.referenceHeight=0.05/self.pad.GetAbsHNDC() *self.pad.GetWw() / self.pad.GetWh()
            #self.referenceHeight = self.pad.GetTopMargin()
        print "decoreferenceheight",self.referenceHeight,0.05,self.pad.GetAbsHNDC() ,self.pad.GetWw() , self.pad.GetWh()

    def Draw(self):
        if type(self.additionalText) is list or self.additionalText is None:
            additionalTextList = self.additionalText
        else:
            additionalTextList = [self.additionalText]
        align_=2
        if self.align=="left":
            align_+=10
        elif self.align=="center":
            align_+=20
        elif self.align=="right":
            align_+=30
    
        l = self.pad.GetLeftMargin()
        t = self.pad.GetTopMargin()
        r = self.pad.GetRightMargin()
        b = self.pad.GetBottomMargin()
        self.pad.cd()
        latex=ROOT.TLatex()
        latex.SetNDC()
        latex.SetTextAngle(0)
        latex.SetTextColor(ROOT.kBlack)
        latex.SetTextFont(42)
        latex.SetTextAlign(31)
        latex.SetTextSize(self.lumiTextSize*self.referenceHeight)
        latex.DrawLatex(1-r,1-t+self.lumiTextOffset*t,self.lumiText)
    
        if self.valign=="outofframe":
            latex.SetTextFont(self.cmsTextFont)
            latex.SetTextAlign(11)
            latex.SetTextSize(self.cmsTextSize*self.referenceHeight)
            latex.DrawLatex(l,1-t+lumiTextOffset*t,"CMS")
            latex.SetTextFont(self.extraTextFont)
            latex.SetTextSize(self.extraTextSize*self.referenceHeight)
            latex.DrawLatex(l +  cmsTextSize*t*extraTextOffset, 1-t+lumiTextOffset*t, extraText)  #this can be improved to the actual cms text size+something
        else:
            latex.SetTextAlign(align_)
            totalTextHeight=self.relExtraDY*self.cmsTextSize*self.referenceHeight
            if self.extraText: totalTextHeight+=self.relExtraDY*self.extraTextSize*self.referenceHeight
            if additionalTextList: totalTextHeight+=len(additionalTextList)*(self.relExtraDY*self.additionalTextSize*self.referenceHeight)+self.additionalTextVspace*self.referenceHeight
            
            if self.align=="left":
                posX_ =   l + self.relPosX*(1-l-r)+self.hspace
            elif( self.align=="center" ):
                posX_ =  l + 0.5*(1-l-r)+self.hspace
            elif( self.align=="right" ):
                posX_ =  1-r - self.relPosX*(1-l-r)+self.hspace
            if self.valign=="top":
                posY_ = 1-t - self.relPosY*(1-t-b)-self.vspace
            elif( self.valign=="middle" ):
                posY_ = b + 0.5*(1-t-b+totalTextHeight) -self.vspace
            elif( self.valign=="bottom" ):
                posY_ = b + self.relPosY*(1-t-b)+totalTextHeight-self.vspace
            posY_-=self.relExtraDY*self.cmsTextSize*self.referenceHeight*0.5
            latex.SetTextFont(self.cmsTextFont)
            latex.SetTextSize(self.cmsTextSize*self.referenceHeight)
            print "settextsize",self.cmsTextSize,self.referenceHeight
            latex.SetTextAlign(align_)
            latex.DrawLatex(posX_, posY_, "CMS")
            posY_-=self.relExtraDY*self.cmsTextSize*self.referenceHeight*0.5
            if( self.extraText ):
                posY_-=self.relExtraDY*self.extraTextSize*self.referenceHeight*0.5
                latex.SetTextFont(self.extraTextFont)
                latex.SetTextAlign(align_)
                latex.SetTextSize(self.extraTextSize*self.referenceHeight)
                latex.DrawLatex(posX_, posY_, self.extraText)
                posY_-=self.relExtraDY*self.extraTextSize*self.referenceHeight*0.5
            if( additionalTextList ):
                posY_-=self.additionalTextVspace*self.referenceHeight
                for text in additionalTextList:
                    posY_-=self.relExtraDY*self.additionalTextSize*self.referenceHeight*0.5
                    latex.SetTextFont(self.additionalTextFont)
                    latex.SetTextAlign(align_)
                    latex.SetTextSize(self.additionalTextSize*self.referenceHeight)
                    latex.DrawLatex(posX_, posY_, text)
                    posY_-=self.relExtraDY*self.additionalTextSize*self.referenceHeight*0.5

def cmsDecoration(extraText=None, additionalText=None, lumiText="19.7 fb^{-1} (8 TeV)", align="left", valign="top", vspace=0, hspace=0):
    cmsTextFont          = 61   # Fonts
    lumiTextFont         = 42
    extraTextFont        = 52
    additionalTextFont   = 42
    cmsTextSize          = 0.9  #Text sizes
    lumiTextSize         = 0.6
    extraTextSize        = 0.76*cmsTextSize
    additionalTextSize   = 1.0*extraTextSize
    additionalTextVspace = 0.3*extraTextSize
    lumiTextOffset       = 0.2
    extraTextOffset      = 2.5  # only used in outOfFrame version

    relPosX    = 0.055  #relative padding
    relPosY    = 0.055
    relExtraDY = 1.3    #line height
    for i in range(1000):
        pad = ROOT.gROOT.GetSelectedPad()
        print pad
        if repr(pad)!="<ROOT.TVirtualPad object at 0x(nil)>": break
    if type(additionalText) is list or additionalText is None:
        additionalTextList = additionalText
    else:
        additionalTextList = [additionalText]
    align_=2
    if align=="left":
        align_+=10
    elif align=="center":
        align_+=20
    elif align=="right":
        align_+=30

    l = pad.GetLeftMargin()
    t = pad.GetTopMargin()
    r = pad.GetRightMargin()
    b = pad.GetBottomMargin()
    pad.cd()

    latex=ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextAngle(0)
    latex.SetTextColor(ROOT.kBlack)


    latex.SetTextFont(42)
    latex.SetTextAlign(31)
    latex.SetTextSize(lumiTextSize*t)
    latex.DrawLatex(1-r,1-t+lumiTextOffset*t,lumiText)

    if valign=="outofframe":
        latex.SetTextFont(cmsTextFont)
        latex.SetTextAlign(11)
        latex.SetTextSize(cmsTextSize*t)
        latex.DrawLatex(l,1-t+lumiTextOffset*t,"CMS")
        latex.SetTextFont(extraTextFont)
        latex.SetTextSize(extraTextSize*t)
        latex.DrawLatex(l +  cmsTextSize*t*extraTextOffset, 1-t+lumiTextOffset*t, extraText)
    else:
        latex.SetTextAlign(align_)
        totalTextHeight=relExtraDY*cmsTextSize*t
        if extraText: totalTextHeight+=relExtraDY*extraTextSize*t
        if additionalTextList: totalTextHeight+=len(additionalTextList)*(relExtraDY*additionalTextSize*t)+additionalTextVspace*t
        
        if align=="left":
          posX_ =   l + relPosX*(1-l-r)+hspace
        elif( align=="center" ):
          posX_ =  l + 0.5*(1-l-r)+hspace
        elif( align=="right" ):
            posX_ =  1-r - relPosX*(1-l-r)+hspace
        if valign=="top":
            posY_ = 1-t - relPosY*(1-t-b)-vspace
        elif( valign=="middle" ):
            posY_ = b + 0.5*(1-t-b+totalTextHeight) -vspace
        elif( valign=="bottom" ):
            posY_ = b + relPosY*(1-t-b)+totalTextHeight-vspace
        posY_-=relExtraDY*cmsTextSize*t*0.5
        latex.SetTextFont(cmsTextFont)
        latex.SetTextSize(cmsTextSize*t)
        latex.SetTextAlign(align_)
        latex.DrawLatex(posX_, posY_, "CMS")
        posY_-=relExtraDY*cmsTextSize*t*0.5
        if( extraText ):
            posY_-=relExtraDY*extraTextSize*t*0.5
            latex.SetTextFont(extraTextFont)
            latex.SetTextAlign(align_)
            latex.SetTextSize(extraTextSize*t)
            latex.DrawLatex(posX_, posY_, extraText)
            posY_-=(relExtraDY)*extraTextSize*t*0.5
        if( additionalTextList ):
            posY_-=additionalTextVspace*t
            for text in additionalTextList:
                posY_-=relExtraDY*additionalTextSize*t*0.5
                latex.SetTextFont(additionalTextFont)
                latex.SetTextAlign(align_)
                latex.SetTextSize(additionalTextSize*t)
                latex.DrawLatex(posX_, posY_, text)
                posY_-=relExtraDY*additionalTextSize*t*0.5
        
class Legend(object):
    #@property
    #def referenceHeight(self):
        #print "heightget",self.pad.GetWh()
        #return self._referenceHeight
    #@referenceHeight.setter
    #def referenceHeight(self, value):
        #print "height",self.pad.GetAbsHNDC()
        #self._referenceHeight = value
    def __init__(self, align="right", valign="top", pad=None, vspace=0, hspace=0,ncolumns=1):
        self.textFont    = 42       #text font
        self.textSize    = 0.6      #relative text size to top margin
        self.tickOffset  = 0.02     #offset for ticks
        self.relPosX     = 0.01#0.055;   #relative padding
        self.relPosY     = 0.01#0.035;   #relative padding
        self.lineHeight  = 1.3      #relative line height of legend
        self.symbolWidth = 0.1      #width of the legend symbol
        self.legendGap   = 0.05     #reserved space for the gap (cannot be tuned)
        self.vspace=vspace
        self.hspace=hspace
        self.ncolumns=ncolumns
        if pad is not None:
            self.pad = pad
        else:
            for i in range(1000):
                self.pad = ROOT.gROOT.GetSelectedPad()
                print self.pad
                if repr(self.pad)!="<ROOT.TVirtualPad object at 0x(nil)>": break
        self.referenceHeight=0.05/self.pad.GetAbsHNDC() *self.pad.GetWw() / self.pad.GetWh()
        print "referenceheight",self.referenceHeight,0.05,self.pad.GetAbsHNDC() ,self.pad.GetWw() , self.pad.GetWh()
        print "Legend pad and Wh",self.pad, self.pad.GetWh()
        self.align, self.valign = align, valign
        self.entries = []
        self.__position=(None, None, None, None)
    def add(self,hist,label,option=""):
        self.entries.append([hist,label,option])
    def AddEntry(self,hist,label,option=""):
        self.add(hist,label,option)
    def getTextWidth(self,text):
        #this will only work with a linear x-axis
        l=ROOT.TLatex()
        l.SetTextFont(self.textFont)
        l.SetTextSize(self.textSize*self.referenceHeight)
        l.SetText(0,0,text)
        return (self.pad.XtoPixel(l.GetXsize())-self.pad.XtoPixel(0))/self.pad.UtoPixel(1)
    def Draw(self):
        self.draw()
    def draw(self):
        #H = self.pad.GetWh()
        #W = self.pad.GetWw()
        l = self.pad.GetLeftMargin()
        t = self.pad.GetTopMargin()
        r = self.pad.GetRightMargin()
        b = self.pad.GetBottomMargin()
        
        textwidth=0
        for e in self.entries:
            print self.getTextWidth(e[1])
            textwidth=max(textwidth, self.getTextWidth(e[1]))
        self.margin=1/(1+textwidth/self.symbolWidth)  # relative symbol width
        legendheight=int((len(self.entries)+1)/self.ncolumns) *self.textSize*self.lineHeight*self.referenceHeight 
        legendwidth =(self.margin+1)*textwidth+self.legendGap 
        if self.valign=="top":
            posy=1-t-legendheight- self.tickOffset - self.relPosY*(1-t-b)
        if self.valign=="bottom":
            posy=b+ self.tickOffset + self.relPosY*(1-t-b)
        if self.valign=="free":
            posy=0
        if self.align=="right":
            posx=1-r-self.tickOffset - self.relPosX*(1-l-r)-legendwidth
        if self.align=="left":
            posx=l+self.tickOffset+self.relPosX*(1-l-r)
        if self.align=="free":
            posx=0
        self.__position=(posx+self.hspace,posy+self.vspace, posx+legendwidth+self.hspace,posy+legendheight+self.vspace)

            
            
            #if self.align=="left":
                #posX_ =   l + self.relPosX*(1-l-r)+self.hspace
            #elif( self.align=="center" ):
                #posX_ =  l + 0.5*(1-l-r)+self.hspace
            #elif( self.align=="right" ):
                #posX_ =  1-r - self.relPosX*(1-l-r)+self.hspace
            #if self.valign=="top":
                #posY_ = 1-t - self.relPosY*(1-t-b)-self.vspace
            #elif( self.valign=="middle" ):
                #posY_ = b + 0.5*(1-t-b+totalTextHeight) -self.vspace
            #elif( self.valign=="bottom" ):
                #posY_ = b + self.relPosY*(1-t-b)+totalTextHeight-self.vspace

            
            
            
        leg=ROOT.TLegend(*(self.__position))
        leg.SetNColumns(self.ncolumns)
        leg.SetFillStyle(0)
        leg.SetBorderSize(0)
        leg.SetFillColor(ROOT.kWhite)
        leg.SetTextFont(self.textFont)
        leg.SetTextSize(self.textSize*self.referenceHeight)
        print "Legend text size",self.textSize*self.referenceHeight
        leg.SetMargin(self.margin)
        for e in self.entries:
            leg.AddEntry(e[0],e[1],e[2])
        leg.Draw()
        self.leg=leg
    x0 = property(lambda self: self.__position[0])
    y0 = property(lambda self: self.__position[1])
    x1 = property(lambda self: self.__position[2])
    y1 = property(lambda self: self.__position[3])
    width = property(lambda self: self.__position[2]-self.__position[0])
    height = property(lambda self: self.__position[3]-self.__position[1])

def tdrStyle():
    tdrStyle = ROOT.TStyle("tdrStyle","Style for P-TDR")

    ## For the canvas:
    tdrStyle.SetCanvasBorderMode(0)
    tdrStyle.SetCanvasColor(ROOT.kWhite)
    tdrStyle.SetCanvasDefH(600) #Height of canvas
    tdrStyle.SetCanvasDefW(600) #Width of canvas
    tdrStyle.SetCanvasDefX(0)   #POsition on screen
    tdrStyle.SetCanvasDefY(0)

    # For the Pad:
    tdrStyle.SetPadBorderMode(0)
    # tdrStyle.SetPadBorderSize(Width_t size = 1)
    tdrStyle.SetPadColor(ROOT.kWhite)
    #tdrStyle.SetPadGridX(1)
    #tdrStyle.SetPadGridY(1)
    tdrStyle.SetGridColor(0)
    tdrStyle.SetGridStyle(3)
    tdrStyle.SetGridWidth(1)

    # For the frame:
    tdrStyle.SetFrameBorderMode(0)
    tdrStyle.SetFrameBorderSize(1)
    tdrStyle.SetFrameFillColor(0)
    tdrStyle.SetFrameFillStyle(0)
    tdrStyle.SetFrameLineColor(1)
    tdrStyle.SetFrameLineStyle(1)
    tdrStyle.SetFrameLineWidth(1)

    # For the histo:
    # tdrStyle.SetHistFillColor(1)
    # tdrStyle.SetHistFillStyle(0)
    tdrStyle.SetHistLineColor(1)
    tdrStyle.SetHistLineStyle(0)
    tdrStyle.SetHistLineWidth(1)
    # tdrStyle.SetLegoInnerR(Float_t rad = 0.5)
    # tdrStyle.SetNumberContours(Int_t number = 20)

    tdrStyle.SetEndErrorSize(2)
    #tdrStyle.SetErrorMarker(20)
    tdrStyle.SetErrorX(.5)

    tdrStyle.SetMarkerStyle(20)

    #For the fit/function:
    tdrStyle.SetOptFit(1)
    tdrStyle.SetFitFormat("5.4g")
    tdrStyle.SetFuncColor(2)
    tdrStyle.SetFuncStyle(1)
    tdrStyle.SetFuncWidth(1)

    #For the date:
    tdrStyle.SetOptDate(0)
    # tdrStyle.SetDateX(Float_t x = 0.01)
    # tdrStyle.SetDateY(Float_t y = 0.01)

    # For the statistics box:
    tdrStyle.SetOptFile(0)
    tdrStyle.SetOptStat(0) # To display the mean and RMS:   SetOptStat("mr")
    tdrStyle.SetStatColor(ROOT.kWhite)
    tdrStyle.SetStatFont(42)
    tdrStyle.SetStatFontSize(0.025)
    tdrStyle.SetStatTextColor(1)
    tdrStyle.SetStatFormat("6.4g")
    tdrStyle.SetStatBorderSize(1)
    tdrStyle.SetStatH(0.1)
    tdrStyle.SetStatW(0.15)
    # tdrStyle.SetStatStyle(Style_t style = 1001)
    # tdrStyle.SetStatX(Float_t x = 0)
    # tdrStyle.SetStatY(Float_t y = 0)

    # Margins:
    tdrStyle.SetPadTopMargin(0.05)
    tdrStyle.SetPadBottomMargin(0.13)
    tdrStyle.SetPadLeftMargin(0.16)
    tdrStyle.SetPadRightMargin(0.05)

    # For the Global title:

    #  tdrStyle.SetOptTitle(0)
    tdrStyle.SetTitleFont(42)
    tdrStyle.SetTitleColor(1)
    tdrStyle.SetTitleTextColor(1)
    tdrStyle.SetTitleFillColor(10)
    tdrStyle.SetTitleFontSize(0.05)
    # tdrStyle.SetTitleH(0) # Set the height of the title box
    # tdrStyle.SetTitleW(0) # Set the width of the title box
    # tdrStyle.SetTitleX(0) # Set the position of the title box
    # tdrStyle.SetTitleY(0.985) # Set the position of the title box
    # tdrStyle.SetTitleStyle(Style_t style = 1001)
    # tdrStyle.SetTitleBorderSize(2)

    # For the axis titles:

    tdrStyle.SetTitleColor(1, "XYZ")
    tdrStyle.SetTitleFont(42, "XYZ")
    tdrStyle.SetTitleSize(0.06, "XYZ")
    # tdrStyle.SetTitleXSize(Float_t size = 0.02) # Another way to set the size?
    # tdrStyle.SetTitleYSize(Float_t size = 0.02)
    tdrStyle.SetTitleXOffset(0.9)
    tdrStyle.SetTitleYOffset(1.25)
    # tdrStyle.SetTitleOffset(1.1, "Y") # Another way to set the Offset

    # For the axis labels:

    tdrStyle.SetLabelColor(1, "XYZ")
    tdrStyle.SetLabelFont(42, "XYZ")
    tdrStyle.SetLabelOffset(0.007, "XYZ")
    tdrStyle.SetLabelSize(0.04, "XYZ")

    # For the axis:

    tdrStyle.SetAxisColor(1, "XYZ")
    tdrStyle.SetStripDecimals(ROOT.kTRUE)
    tdrStyle.SetTickLength(0.03, "XYZ")
    tdrStyle.SetNdivisions(510, "XYZ")
    tdrStyle.SetPadTickX(1)  # To get tick marks on the opposite side of the frame
    tdrStyle.SetPadTickY(1)

    # Change for log plots:
    tdrStyle.SetOptLogx(0)
    tdrStyle.SetOptLogy(0)
    tdrStyle.SetOptLogz(0)

    # Postscript options:
    # tdrStyle.SetPaperSize(15.,15.)
    # tdrStyle.SetLineScalePS(Float_t scale = 3)
    # tdrStyle.SetLineStyleString(Int_t i, const char* text)
    # tdrStyle.SetHeaderPS(const char* header)
    # tdrStyle.SetTitlePS(const char* pstitle)

    # tdrStyle.SetBarOffset(Float_t baroff = 0.5)
    # tdrStyle.SetBarWidth(Float_t barwidth = 0.5)
    # tdrStyle.SetPaintTextFormat(const char* format = "g")
    # tdrStyle.SetPalette(Int_t ncolors = 0, Int_t* colors = 0)
    # tdrStyle.SetTimeOffset(Double_t toffset)
    # tdrStyle.SetHistMinimumZero(ROOT.kTRUE)

    tdrStyle.cd()
    return tdrStyle
