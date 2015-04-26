from ROOT import Double

class BasePlottable(object) :
  '''Base class for plottable objects'''
  def __init__( self, name ) :
    self.name = name

  # Require children to implement these
  def number_of_points( self ) :
    raise NotImplementedError( 'number_of_points not defined by {0}'.format(type(self)) )

  def draw_on_plot( self, plot, **kwargs ) :
    raise NotImplementedError( 'draw_on_plot not defined by {0}'.format(type(self)) )

  # Constructors
  @classmethod
  def from_x_edges_y_values( cls, x_bin_edges, y_values, y_error_pairs ) :
    x_values = [ 0.5*(low_edge+high_edge) for low_edge, high_edge in zip( x_bin_edges[:-1], x_bin_edges[1:] ) ]
    x_error_pairs = [ (centre-low_edge,centre-low_edge) for centre, low_edge in zip(x_values,x_bin_edges[:-1]) ]
    return cls( x_values, x_error_pairs, y_values, y_error_pairs )

  @classmethod
  def from_TH1( cls, input_TH1 ) :
    x_bin_edges = [ input_TH1.GetBinLowEdge(bin) for bin in range(1,input_TH1.GetNbinsX()+2) ]
    y_values = [ input_TH1.GetBinContent(bin) for bin in range(1,input_TH1.GetNbinsX()+1) ]
    y_error_pairs = [ (input_TH1.GetBinError(bin),input_TH1.GetBinError(bin)) for bin in range(1,input_TH1.GetNbinsX()+1) ]
    return cls.from_x_edges_y_values( x_bin_edges, y_values, y_error_pairs )

  @classmethod
  def from_TGraphAsymmErrors( cls, input_TGraphAsymmErrors ) :
    x_values, x_errors, y_values, y_errors = [], [], [], []
    for point in range( input_TGraphAsymmErrors.GetN() ) :
      x, y = Double(), Double()
      input_TGraphAsymmErrors.GetPoint( point, x, y )
      x_values.append( x )
      y_values.append( y )
      x_errors.append( (input_TGraphAsymmErrors.GetErrorXlow(point),input_TGraphAsymmErrors.GetErrorXhigh(point)) )
      y_errors.append( (input_TGraphAsymmErrors.GetErrorYlow(point),input_TGraphAsymmErrors.GetErrorYhigh(point)) )
    return cls( x_values, x_errors, y_values, y_errors )



