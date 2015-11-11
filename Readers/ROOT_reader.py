import numpy as np
import ROOT

## Interpreter for ROOT objects
class ROOTReader(object) :
  def __init__( self, root_object ) :
    self.x_values, self.x_error_pairs = None, None
    self.y_values, self.y_error_pairs = None, None
    self.z_values, self.z_error_pairs = None, None
    # Initialise TH2 constructor
    if isinstance( root_object, ROOT.TH2 ) :
      self.construct_from_TH2( root_object )
    # Initialise TH1 constructor
    elif isinstance( root_object, ROOT.TH1 ) :
      self.construct_from_TH1( root_object )
    # Initialise TGraphAsymmErrors constructor
    elif isinstance( root_object, ROOT.TGraphAsymmErrors ) :
      self.construct_from_TGraphAsymmErrors( root_object )
    # Initialise TGraphErrors constructor
    elif isinstance( root_object, ROOT.TGraphErrors ) :
      self.construct_from_TGraphErrors( root_object )
    # Initialise TGraph constructor
    elif isinstance( root_object, ROOT.TGraph ) :
      self.construct_from_TGraph( root_object )
    else :
      raise NotImplementedError( 'Constructor signature {0}, {1} not known'.format( *args, **kwargs ) )


  ## Read TH1 into x, y dimensions
  def construct_from_TH1( self, input_TH1 ) :
    self.x_values = [ input_TH1.GetXaxis().GetBinCenter(bin) for bin in range(1,input_TH1.GetNbinsX()+1) ]
    self.x_error_pairs = [ [ 0.5*input_TH1.GetXaxis().GetBinWidth(bin) ]*2 for bin in range(1,input_TH1.GetNbinsX()+1) ]
    self.y_values = [ input_TH1.GetBinContent(bin) for bin in range(1,input_TH1.GetNbinsX()+1) ]
    self.y_error_pairs = [ (input_TH1.GetBinErrorLow(bin),input_TH1.GetBinErrorUp(bin)) for bin in range(1,input_TH1.GetNbinsX()+1) ]


  ## Read TH2 into x, y, z dimensions
  def construct_from_TH2( self, input_TH2 ) :
    self.x_values = [ input_TH2.GetXaxis().GetBinCenter(bin) for bin in range(1,input_TH2.GetNbinsX()+1) ]
    self.x_error_pairs = [ [ 0.5*input_TH2.GetXaxis().GetBinWidth(bin) ]*2 for bin in range(1,input_TH2.GetNbinsX()+1) ]
    self.y_values = [ input_TH2.GetYaxis().GetBinCenter(bin) for bin in range(1,input_TH2.GetNbinsY()+1) ]
    self.y_error_pairs = [ [ 0.5*input_TH2.GetYaxis().GetBinWidth(bin) ]*2 for bin in range(1,input_TH2.GetNbinsY()+1) ]
    self.z_values, self.z_error_pairs = [], []
    x_bin_edges = [ input_TH2.GetXaxis().GetBinLowEdge(bin) for bin in range(1,input_TH2.GetNbinsX()+2) ]
    y_bin_edges = [ input_TH2.GetYaxis().GetBinLowEdge(bin) for bin in range(1,input_TH2.GetNbinsY()+2) ]
    ix_array, iy_array = np.meshgrid( range(1,len(x_bin_edges)), range(1,len(y_bin_edges)), indexing='xy' )
    for ix, iy in zip( ix_array.ravel(), iy_array.ravel() ) :
      self.z_values.append( input_TH2.GetBinContent(ix,iy) )
      self.z_error_pairs.append( (input_TH2.GetBinErrorLow(ix,iy),input_TH2.GetBinErrorUp(ix,iy)) )


  ## Read TGraph into x, y dimensions
  def construct_from_TGraph( self, input_TGraph ) :
    x, x_errors = input_TGraphAsymmErrors.GetX(), input_TGraphAsymmErrors.GetEX()
    y, y_errors = input_TGraphAsymmErrors.GetY(), input_TGraphAsymmErrors.GetEY()
    self.x_values, self.x_error_pairs, self.y_values, self.y_error_pairs = [], [], [], []
    for ii in range( input_TGraphAsymmErrors.GetN() ) :
      self.x_values.append( x[ii] )
      self.x_error_pairs.append( [x_errors[ii]]*2 )
      self.y_values.append( y[ii] )
      self.y_error_pairs.append( [y_errors[ii]]*2 )


  ## Read TGraphErrors into x, y dimensions
  def construct_from_TGraphErrors( self, input_TGraphErrors ) :
    x, x_errors = input_TGraphAsymmErrors.GetX(), input_TGraphAsymmErrors.GetEX()
    y, y_errors = input_TGraphAsymmErrors.GetY(), input_TGraphAsymmErrors.GetEY()
    self.x_values, self.x_error_pairs, self.y_values, self.y_error_pairs = [], [], [], []
    for ii in range( input_TGraphAsymmErrors.GetN() ) :
      self.x_values.append( x[ii] )
      self.x_error_pairs.append( [x_errors[ii]]*2 )
      self.y_values.append( y[ii] )
      self.y_error_pairs.append( [y_errors[ii]]*2 )


  ## Read TGraphErrors into x, y dimensions
  def construct_from_TGraphAsymmErrors( self, input_TGraphAsymmErrors ) :
    x, x_errors_low, x_errors_high = input_TGraphAsymmErrors.GetX(), input_TGraphAsymmErrors.GetEXlow(), input_TGraphAsymmErrors.GetEXhigh()
    y, y_errors_low, y_errors_high = input_TGraphAsymmErrors.GetY(), input_TGraphAsymmErrors.GetEYlow(), input_TGraphAsymmErrors.GetEYhigh()
    self.x_values, self.x_error_pairs, self.y_values, self.y_error_pairs = [], [], [], []
    for ii in range( input_TGraphAsymmErrors.GetN() ) :
      self.x_values.append( x[ii] + ( x_errors_high[ii] - x_errors_low[ii] ) / 2.0 )
      self.x_error_pairs.append( [(x_errors_high[ii] + x_errors_low[ii])/2.0]*2 )
      self.y_values.append( y[ii] + ( y_errors_high[ii] - y_errors_low[ii] ) / 2.0 )
      self.y_error_pairs.append( [(y_errors_high[ii] + y_errors_low[ii])/2.0]*2 )
