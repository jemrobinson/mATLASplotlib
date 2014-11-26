class BasePlottable(object) :
  '''Base class for plottable objects'''
  def __init__( self, name ) :
    self.name = name

  def number_of_points( self ) :
    raise NotImplementedError( 'number_of_points not defined by {0}'.format(type(self)) )

  def draw_on_plot( self, plot, **kwargs ) :
    raise NotImplementedError( 'draw_on_plot not defined by {0}'.format(type(self)) )

  def number_of_points( self ) :
    raise NotImplementedError( 'number_of_points not defined by {0}'.format(type(self)) )


  def from_x_edges_y_values( self, x_bin_edges, y_values, y_error_pairs ) :
    x_centres = [ 0.5*(low_edge+high_edge) for low_edge, high_edge in zip( x_bin_edges[:-1], x_bin_edges[1:] ) ]
    x_errors = [ centre-low_edge for centre, low_edge in zip(x_centres,x_bin_edges[:-1]) ]
    self.__construct__( x_values, x_errors, y_values, y_errors )

  def from_TH1( self, input_TH1 ) :
    x_bin_edges = [ input_TH1.GetBinLowEdge(bin) for bin in range(1,input_TH1.GetNbinsX()+2) ]
    y_values = [ input_TH1.GetBinContent(bin) for bin in range(1,input_TH1.GetNbinsX()+1) ]
    y_error_pairs = [ (input_TH1.GetBinError(bin),input_TH1.GetBinError(bin)) for bin in range(1,input_TH1.GetNbinsX()+1) ]
    self.__construct__( x_values, x_errors, y_values, y_error_pairs )

# plt.hist(x, 50, normed=1, facecolor='green', alpha=0.75)
  # def from_TH1( self, input_TH1 ) :
  #   x_bin_edges = [ input_TH1.GetBinLowEdge(bin) for bin in range(1,input_TH1.GetNbinsX()+2) ]
  #   y_values = [ input_TH1.GetBinContent(bin) for bin in range(1,input_TH1.GetNbinsX()+1) ]
  #   y_error_pairs = [ (input_TH1.GetBinError(bin),input_TH1.GetBinError(bin)) for bin in range(1,input_TH1.GetNbinsX()+1) ]
  #   self.__construct__( x_bin_edges, y_values, y_error_pairs )
