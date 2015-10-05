import numpy as np

class BasePlottable(object) :
  '''Base class for plottable objects'''

  ## Constructor - specify values and error pair separately for each dimension
  # Example : x vs y : __init__( x_values = [1,2,3], y_values = [1,4,9] )
  def __init__( self, *args, **kwargs ) :
    self._data = {}
    # Use a configurator object to construct
    if len(args) == 1 :
      if hasattr( args[0], 'x_values' ) and getattr( args[0], 'x_values' ) is not None : self.add_dimension( 'x', args[0].x_values, args[0].x_error_pairs )
      if hasattr( args[0], 'y_values' ) and getattr( args[0], 'y_values' ) is not None : self.add_dimension( 'y', args[0].y_values, args[0].y_error_pairs )
      if hasattr( args[0], 'z_values' ) and getattr( args[0], 'z_values' ) is not None : self.add_dimension( 'z', args[0].z_values, args[0].z_error_pairs )
    # Assume that x,y values have been passed
    elif len(args) == 2 :
      self.add_dimension( 'x', args[0], None )
      self.add_dimension( 'y', args[1], None )
    # Assume that x,y,z values have been passed
    elif len(args) == 3 :
      self.add_dimension( 'x', args[0], None )
      self.add_dimension( 'y', args[1], None )
      self.add_dimension( 'z', args[2], None )
    # Assume that x,y values with errors have been passed
    elif len(args) == 4 :
      self.add_dimension( 'x', args[0], args[1] )
      self.add_dimension( 'y', args[2], args[3] )
    # Assume that x,y,z values with errors have been passed
    elif len(args) == 6 :
      self.add_dimension( 'x', args[0], args[1] )
      self.add_dimension( 'y', args[2], args[3] )
      self.add_dimension( 'z', args[4], args[5] )
    # Construct an array of points in N-dimensional space, with an error pair in each direction
    else :
      if 'x_values' in kwargs : self.add_dimension( 'x', kwargs['x_values'], kwargs.get('x_error_pairs',None) )
      if 'y_values' in kwargs : self.add_dimension( 'y', kwargs['y_values'], kwargs.get('y_error_pairs',None) )
      if 'z_values' in kwargs : self.add_dimension( 'z', kwargs['z_values'], kwargs.get('z_error_pairs',None) )
      for dimension in self.get_dimensions() : assert( len(self._data[dimension]) == self.number_of_points() )
    if 'x' in self.get_dimensions() and 'y' in self.get_dimensions() :
      self.add_xy_dimensions()


  def number_of_points( self ) :
    return len( self._data[self.get_dimensions()[0]] )


  def get_dimensions( self ) :
    return sorted( self._data.keys() )


  ## Add a new dimension with appropriate methods
  def add_dimension( self, dimension, values, error_pairs ) :
    if error_pairs is None : error_pairs = [ (0,0) ] * len(values)
    assert( len(values) == len(error_pairs) )
    self._data[dimension] = np.array( [ [ value, error_pair[0], error_pair[1] ] for value, error_pair in zip( values, error_pairs ) ] )
    setattr( self, '{0}_points'.format(dimension), self.__get_points(dimension) )
    setattr( self, '{0}_error_pairs'.format(dimension), self.__get_error_pairs(dimension) )
    setattr( self, '{0}_points_error_symmetrised'.format(dimension), self.__get_points_error_symmetrised(dimension) )
    setattr( self, '{0}_errors_symmetrised'.format(dimension), self.__get_errors_symmetrised(dimension) )
    setattr( self, '{0}_bin_edges'.format(dimension), self.__get_bin_edges(dimension) )
    setattr( self, '{0}_unique_bin_edges'.format(dimension), self.__get_unique_bin_edges(dimension) )
    setattr( self, '{0}_bin_widths'.format(dimension), self.__get_bin_widths(dimension) )
    setattr( self, '{0}_bin_low_edges'.format(dimension), self.__get_bin_low_edges(dimension) )
    setattr( self, '{0}_bin_high_edges'.format(dimension), self.__get_bin_high_edges(dimension) )


  ## Add xy-appropriate methods
  def add_xy_dimensions(self) :
    setattr( self, 'x_at_y_bin_edges',  self.__get_x_at_y_bin_edges() )
    setattr( self, 'y_at_x_bin_edges',  self.__get_y_at_x_bin_edges() )
    setattr( self, 'band_edges_x',      self.__get_band_edges_x() )
    setattr( self, 'band_edges_y_low',  self.__get_band_edges_y_low() )
    setattr( self, 'band_edges_y_high', self.__get_band_edges_y_high() )


  ## Return array of x/y/z points, constructing if necessary
  def __get_points( self, dimension ) :
    attr_name = '_{0}_points'.format(dimension)
    if not hasattr( self, attr_name ) :
      value = np.array( [ point[0] for point in self._data[dimension] ] )
      setattr( self, attr_name, value )
    return getattr( self, attr_name )


  ## Return array of x/y/z points, constructing if necessary
  def __get_error_pairs( self, dimension ) :
    attr_name = '_{0}_error_pairs'.format(dimension)
    if not hasattr( self, attr_name ) :
      value = np.array( [ [point[1],point[2]] for point in self._data[dimension] ] )
      setattr( self, attr_name, value )
    return getattr( self, attr_name )


  ## Return array of x/y/z points, constructing if necessary
  def __get_points_error_symmetrised( self, dimension ) :
    attr_name = '_{0}_points_error_symmetrised'.format(dimension)
    if not hasattr( self, attr_name ) :
      value = np.array( [ point[0]+(point[2]-point[1])/2.0 for point in self._data[dimension] ] )
      setattr( self, attr_name, value )
    return getattr( self, attr_name )


  ## Return array of x/y/z points, constructing if necessary
  def __get_errors_symmetrised( self, dimension ) :
    attr_name = '_{0}_errors_symmetrised'.format(dimension)
    if not hasattr( self, attr_name ) :
      value = np.array( [ (point[1]+point[2])/2.0 for point in self._data[dimension] ] )
      setattr( self, attr_name, value )
    return getattr( self, attr_name )

  ## Return array of x/y/z bin edges, constructing if necessary
  def __get_bin_edges( self, dimension ) :
    attr_name = '_{0}_bin_edges'.format(dimension)
    if not hasattr( self, attr_name ) :
      value = np.array( sum( [ [low_edge,high_edge] for low_edge, high_edge in zip(self.__get_bin_low_edges(dimension), self.__get_bin_high_edges(dimension)) ], [] ) )
      setattr( self, attr_name, value )
    return getattr( self, attr_name )


  ## Return array of x/y/z bin edges without duplicates, constructing if necessary
  def __get_unique_bin_edges( self, dimension ) :
    attr_name = '_{0}_unique_bin_edges'.format(dimension)
    if not hasattr( self, attr_name ) :
      value = np.unique( getattr( self, '_{0}_bin_edges'.format(dimension) ) )
      setattr( self, attr_name, value )
    return getattr( self, attr_name )


  ## Return array of x/y/z bin widths, constructing if necessary
  def __get_bin_widths( self, dimension ) :
    attr_name = '_{0}_bin_widths'.format(dimension)
    if not hasattr( self, attr_name ) :
      value = np.array( [ point[1] + point[2] for point in self._data[dimension] ] )
      setattr( self, attr_name, value )
    return getattr( self, attr_name )


  ## Return array of x/y/z bin low edges, constructing if necessary
  def __get_bin_low_edges( self, dimension ) :
    attr_name = '_{0}_bin_low_edges'.format(dimension)
    if not hasattr( self, attr_name ) :
      value = np.array( [ point[0] - point[1] for point in self._data[dimension] ] )
      setattr( self, attr_name, value )
    return getattr( self, attr_name )


  ## Return array of x/y/z bin high edges, constructing if necessary
  def __get_bin_high_edges( self, dimension ) :
    attr_name = '_{0}_bin_high_edges'.format(dimension)
    if not hasattr( self, attr_name ) :
      value = np.array( [ point[0] + point[2] for point in self._data[dimension] ] )
      setattr( self, attr_name, value )
    return getattr( self, attr_name )


  ## Return array of x at the bin edges of y bins, constructing if necessary
  def __get_x_at_y_bin_edges( self ) :
    if not hasattr( self, '_x_at_y_bin_edges' ) :
      self._x_at_y_bin_edges = np.array( sum( [ [x_point,x_point] for x_point in self.x_points], [] ) )
    return self._x_at_y_bin_edges


  ## Return array of y at the bin edges of x bins, constructing if necessary
  def __get_y_at_x_bin_edges( self ) :
    if not hasattr( self, '_y_at_x_bin_edges' ) :
      self._y_at_x_bin_edges = np.array( sum( [ [y_point,y_point] for y_point in self.y_points], [] ) )
    return self._y_at_x_bin_edges


  ## Return array of x edges for fillable band, constructing if necessary
  def __get_band_edges_x( self ) :
    if not hasattr( self, '_band_edges_x' ) :
      self._band_edges_x = np.array( sum( [ [ point[0]-point[1], point[0]+point[2] ] for point in self._data['x'] ], [] ) )
    return self._band_edges_x
  #     self.x_points = np.array( sum([ [value-errors[0],value+errors[1]] for value,errors in zip( x_values, x_error_pairs ) ], [] ) )


  ## Return array of y minima for fillable band, constructing if necessary
  def __get_band_edges_y_low( self ) :
    if not hasattr( self, '_band_edges_y_low' ) :
      self._band_edges_y_low = np.array( sum( [ [ point[0]-point[1], point[0]-point[1] ] for point in self._data['y'] ], [] ) )
    return self._band_edges_y_low
  #     self.y_points_l = np.array( sum([ [value-errors[0],value-errors[0]] for value,errors in zip( y_values, y_error_pairs ) ], [] ) )


  ## Return array of y maxima for fillable band, constructing if necessary
  def __get_band_edges_y_high( self ) :
    if not hasattr( self, '_band_edges_y_high' ) :
      self._band_edges_y_high = np.array( sum( [ [ point[0]+point[2], point[0]+point[2] ] for point in self._data['y'] ], [] ) )
    return self._band_edges_y_high
  #     self.y_points_h = np.array( sum([ [value+errors[1],value+errors[1]] for value,errors in zip( y_values, y_error_pairs ) ], [] ) )


# #   def centres_to_edges( self, bin_centres ) :
# #     return [ 2*bin_edges[0] - bin_edges[1] ] + bin_edges + [ 2*bin_edges[-1] - bin_edges[-2] ]
#
# #     # Check whether default constructor is applicable
# #     if len(args) == 4 and len(kwargs) == 0 :
# #       self.construct_from_values_errors( *args )
# #     # Check whether histogram edges/values are provided
# #     elif len(args) == 3 and len(kwargs) == 0 :
# #       self.construct_from_x_edges_y_values( *args )
# #     # Check whether a ROOT object is passed
# #     elif len(args) == 1 :
# #       # Initialise TH2 constructor
# #       if isinstance( args[0], ROOT.TH2 ) :
# #         self.construct_from_TH2( args[0] )
# #       # Initialise TH1 constructor
# #       elif isinstance( args[0], ROOT.TH1 ) :
# #         self.construct_from_TH1( args[0] )
# #       # Initialise TGraphAsymmErrors constructor
# #       elif isinstance( args[0], ROOT.TGraphAsymmErrors ) :
# #         self.construct_from_TGraphAsymmErrors( args[0] )
# #       # Initialise TGraphErrors constructor
# #       elif isinstance( args[0], ROOT.TGraphErrors ) :
# #         self.construct_from_TGraphErrors( args[0] )
# #       # Initialise TGraph constructor
# #       elif isinstance( args[0], ROOT.TGraph ) :
# #         self.construct_from_TGraph( args[0] )
# #     else :
# #       raise NotImplementedError( 'Constructor signature {0}, {1} not known'.format( *args, **kwargs ) )
# #
# #
# #
# #
# #   # Require children to implement this
# #   def draw_on_plot( self, plot, **kwargs ) :
# #     raise NotImplementedError( 'draw_on_plot not defined by {0}'.format( type(self) ) )
# #
# #
# #   ## Utility functions
# #   def edges_to_centres( self, bin_edges ) :
# #     return [ 0.5*(low_edge+high_edge) for low_edge, high_edge in zip( bin_edges[:-1], bin_edges[1:] ) ]
# #
# #   def centres_to_edges( self, bin_centres ) :
# #     bin_edges = [ 0.5*(low_centre+high_centre) for low_centre, high_centre in zip( bin_centres[:-1], bin_centres[1:] ) ]
# #     return [ 2*bin_edges[0] - bin_edges[1] ] + bin_edges + [ 2*bin_edges[-1] - bin_edges[-2] ]
# #
# #
# #   # Constructors
# #   @classmethod
# #   def construct_from_values_errors( cls, x_values=None, x_error_pairs=None, y_values=None, y_error_pairs=None ) :
# #     raise NotImplementedError( 'construct_from_values_errors not defined by {0}'.format( type(self) ) )
# #
# #
# #   def construct_from_x_edges_y_values( self, x_bin_edges, y_values, y_error_pairs ) :
# #     x_values = [ 0.5*(low_edge+high_edge) for low_edge, high_edge in zip( x_bin_edges[:-1], x_bin_edges[1:] ) ]
# #     x_error_pairs = [ (centre-low_edge,centre-low_edge) for centre, low_edge in zip(x_values,x_bin_edges[:-1]) ]
# #     self.construct_from_values_errors( x_values, x_error_pairs, y_values, y_error_pairs )
# #
# #
# #   def construct_from_TH1( self, input_TH1 ) :
# #     x_bin_edges = [ input_TH1.GetBinLowEdge(bin) for bin in range(1,input_TH1.GetNbinsX()+2) ]
# #     y_values = [ input_TH1.GetBinContent(bin) for bin in range(1,input_TH1.GetNbinsX()+1) ]
# #     y_error_pairs = [ (input_TH1.GetBinError(bin),input_TH1.GetBinError(bin)) for bin in range(1,input_TH1.GetNbinsX()+1) ]
# #     self.construct_from_x_edges_y_values( x_bin_edges, y_values, y_error_pairs )
# #
# #
# #   def construct_from_TH2( self, input_TH2 ) :
# #     raise NotImplementedError( 'ROOT.TH2 constructor not defined by {0}'.format( type(self) ) )
# #
# #
# #   def construct_from_TGraph( self, input_TGraph ) :
# #     x, x_errors = input_TGraphAsymmErrors.GetX(), input_TGraphAsymmErrors.GetEX()
# #     y, y_errors = input_TGraphAsymmErrors.GetY(), input_TGraphAsymmErrors.GetEY()
# #     x_values, x_errors, y_values, y_errors = [], [], [], []
# #     for ii in range( input_TGraphAsymmErrors.GetN() ) :
# #       x_values.append( x[ii] )
# #       x_errors.append( (x_errors[ii],x_errors[ii]) )
# #       y_values.append( y[ii] )
# #       y_errors.append( (y_errors[ii],y_errors[ii]) )
# #     self.construct_from_values_errors( x_values, x_errors, y_values, y_errors )
# #
# #
# #   def construct_from_TGraphErrors( self, input_TGraphErrors ) :
# #     x, x_errors = input_TGraphAsymmErrors.GetX(), input_TGraphAsymmErrors.GetEX()
# #     y, y_errors = input_TGraphAsymmErrors.GetY(), input_TGraphAsymmErrors.GetEY()
# #     x_values, x_errors, y_values, y_errors = [], [], [], []
# #     for ii in range( input_TGraphAsymmErrors.GetN() ) :
# #       x_values.append( x[ii] )
# #       x_errors.append( (x_errors[ii],x_errors[ii]) )
# #       y_values.append( y[ii] )
# #       y_errors.append( (y_errors[ii],y_errors[ii]) )
# #     self.construct_from_values_errors( x_values, x_errors, y_values, y_errors )
# #
# #
# #   def construct_from_TGraphAsymmErrors( self, input_TGraphAsymmErrors ) :
# #     x, x_errors_low, x_errors_high = input_TGraphAsymmErrors.GetX(), input_TGraphAsymmErrors.GetEXlow(), input_TGraphAsymmErrors.GetEXhigh()
# #     y, y_errors_low, y_errors_high = input_TGraphAsymmErrors.GetY(), input_TGraphAsymmErrors.GetEYlow(), input_TGraphAsymmErrors.GetEYhigh()
# #     x_values, x_errors, y_values, y_errors = [], [], [], []
# #     for ii in range( input_TGraphAsymmErrors.GetN() ) :
# #       x_values.append( x[ii] + ( x_errors_high[ii] - x_errors_low[ii] ) / 2.0 )
# #       ex = ( x_errors_high[ii] + x_errors_low[ii] ) / 2.0
# #       x_errors.append( (ex,ex) )
# #       y_values.append( y[ii] + ( y_errors_high[ii] - y_errors_low[ii] ) / 2.0 )
# #       ey = ( y_errors_high[ii] + y_errors_low[ii] ) / 2.0
# #       y_errors.append( (ey,ey) )
# #     self.construct_from_values_errors( x_values, x_errors, y_values, y_errors )
