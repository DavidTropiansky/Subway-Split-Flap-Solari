sf.display.ImageDrum = function() {
  return [
    ' ','0',
    '1', '2', '3', '4', '5', '6', '6X', '7', '7X',
    'A', 'B', 'C', 'D', 'E', 'F', 'FX', 'G', 'H', 'J',
    'L', 'M', 'N', 'Q', 'R', 'GS', 'FS', 'T',
    'V', 'W', 'Z',
  ];
};

sf.plugins.arrivals = {
  dataType: 'json',

  url: function(options) {
    return 'api/arrivals';
  },

  formatData: function(response) {
    return response.data;
  }
};
