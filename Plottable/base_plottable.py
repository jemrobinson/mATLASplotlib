from ROOT import TH1, TH2, TGraph, TGraphErrors, TGraphAsymmErrors
import numpy as np

class BasePlottable(object) :
  '''Base class for plottable objects'''
  def __init__( self, *args, **kwargs ) :
    # Check whether default constructor is applicable
    if len(args) == 4 and len(kwargs) == 0 :
      self.construct_from_values_errors( *args )
    # Check whether histogram edges/values are provided
    elif len(args) == 3 and len(kwargs) == 0 :
      self.construct_from_x_edges_y_values( *args )
    # Check whether a ROOT object is passed
    elif len(args) == 1 :
      # Initialise TH2 constructor
      if isinstance( args[0], TH2 ) :
        self.construct_from_TH2( args[0] )
      # Initialise TH1 constructor
      elif isinstance( args[0], TH1 ) :
        self.construct_from_TH1( args[0] )
      # Initialise TGraphAsymmErrors constructor
      elif isinstance( args[0], TGraphAsymmErrors ) :
        self.construct_from_TGraphAsymmErrors( args[0] )
      # Initialise TGraphErrors constructor
      elif isinstance( args[0], TGraphErrors ) :
        self.construct_from_TGraphErrors( args[0] )
      # Initialise TGraph constructor
      elif isinstance( args[0], TGraph ) :
        self.construct_from_TGraph( args[0] )
    else :
      raise NotImplementedError( 'Constructor signature {0}, {1} not known'.format( *args, **kwargs ) )


  # Require children to implement this
  def number_of_points( self ) :
    raise NotImplementedError( 'number_of_points not defined by {0}'.format( type(self) ) )


  # Require children to implement this
  def draw_on_plot( self, plot, **kwargs ) :
    raise NotImplementedError( 'draw_on_plot not defined by {0}'.format( type(self) ) )


  ## Utility functions
  def edges_to_centres( self, bin_edges ) :
    return [ 0.5*(low_edge+high_edge) for low_edge, high_edge in zip( bin_edges[:-1], bin_edges[1:] ) ]

  def centres_to_edges( self, bin_centres ) :
    bin_edges = [ 0.5*(low_centre+high_centre) for low_centre, high_centre in zip( bin_centres[:-1], bin_centres[1:] ) ]
    return [ 2*bin_edges[0] - bin_edges[1] ] + bin_edges + [ 2*bin_edges[-1] - bin_edges[-2] ]


  # Constructors
  @classmethod
  def construct_from_values_errors( cls, x_values=None, x_error_pairs=None, y_values=None, y_error_pairs=None ) :
    raise NotImplementedError( 'construct_from_values_errors not defined by {0}'.format( type(self) ) )


  def construct_from_x_edges_y_values( self, x_bin_edges, y_values, y_error_pairs ) :
    x_values = [ 0.5*(low_edge+high_edge) for low_edge, high_edge in zip( x_bin_edges[:-1], x_bin_edges[1:] ) ]
    x_error_pairs = [ (centre-low_edge,centre-low_edge) for centre, low_edge in zip(x_values,x_bin_edges[:-1]) ]
    self.construct_from_values_errors( x_values, x_error_pairs, y_values, y_error_pairs )


  def construct_from_TH1( self, input_TH1 ) :
    x_bin_edges = [ input_TH1.GetBinLowEdge(bin) for bin in range(1,input_TH1.GetNbinsX()+2) ]
    y_values = [ input_TH1.GetBinContent(bin) for bin in range(1,input_TH1.GetNbinsX()+1) ]
    y_error_pairs = [ (input_TH1.GetBinError(bin),input_TH1.GetBinError(bin)) for bin in range(1,input_TH1.GetNbinsX()+1) ]
    self.construct_from_x_edges_y_values( x_bin_edges, y_values, y_error_pairs )


  def construct_from_TH2( self, input_TH2 ) :
    raise NotImplementedError( 'ROOT.TH2 constructor not defined by {0}'.format( type(self) ) )


  def construct_from_TGraph( self, input_TGraph ) :
    x, x_errors = input_TGraphAsymmErrors.GetX(), input_TGraphAsymmErrors.GetEX()
    y, y_errors = input_TGraphAsymmErrors.GetY(), input_TGraphAsymmErrors.GetEY()
    x_values, x_errors, y_values, y_errors = [], [], [], []
    for ii in range( input_TGraphAsymmErrors.GetN() ) :
      x_values.append( x[ii] )
      x_errors.append( (x_errors[ii],x_errors[ii]) )
      y_values.append( y[ii] )
      y_errors.append( (y_errors[ii],y_errors[ii]) )
    self.construct_from_values_errors( x_values, x_errors, y_values, y_errors )


  def construct_from_TGraphErrors( self, input_TGraphErrors ) :
    x, x_errors = input_TGraphAsymmErrors.GetX(), input_TGraphAsymmErrors.GetEX()
    y, y_errors = input_TGraphAsymmErrors.GetY(), input_TGraphAsymmErrors.GetEY()
    x_values, x_errors, y_values, y_errors = [], [], [], []
    for ii in range( input_TGraphAsymmErrors.GetN() ) :
      x_values.append( x[ii] )
      x_errors.append( (x_errors[ii],x_errors[ii]) )
      y_values.append( y[ii] )
      y_errors.append( (y_errors[ii],y_errors[ii]) )
    self.construct_from_values_errors( x_values, x_errors, y_values, y_errors )


  def construct_from_TGraphAsymmErrors( self, input_TGraphAsymmErrors ) :
    x, x_errors_low, x_errors_high = input_TGraphAsymmErrors.GetX(), input_TGraphAsymmErrors.GetEXlow(), input_TGraphAsymmErrors.GetEXhigh()
    y, y_errors_low, y_errors_high = input_TGraphAsymmErrors.GetY(), input_TGraphAsymmErrors.GetEYlow(), input_TGraphAsymmErrors.GetEYhigh()
    x_values, x_errors, y_values, y_errors = [], [], [], []
    for ii in range( input_TGraphAsymmErrors.GetN() ) :
      x_values.append( x[ii] + ( x_errors_high[ii] - x_errors_low[ii] ) / 2.0 )
      ex = ( x_errors_high[ii] + x_errors_low[ii] ) / 2.0
      x_errors.append( (ex,ex) )
      y_values.append( y[ii] + ( y_errors_high[ii] - y_errors_low[ii] ) / 2.0 )
      ey = ( y_errors_high[ii] + y_errors_low[ii] ) / 2.0
      y_errors.append( (ey,ey) )
    self.construct_from_values_errors( x_values, x_errors, y_values, y_errors )
