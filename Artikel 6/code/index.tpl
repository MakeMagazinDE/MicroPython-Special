{% args data %}
<html>
  <head>
    <title>CO2-Server</title>
    <script src="static/gauge.min.js"></script>
  </head>
  <body>
    <canvas data-type="radial-gauge"
        data-width="300"
        data-height="300"
        data-units="ppm"
        data-title="CO&#8322;"
        data-value="{{data['co2']}}"
        data-min-value="0"
        data-max-value="10000"
        data-major-ticks="[0,1000,2000,3000,4000,5000,6000,7000,8000,9000,10000]"
        data-minor-ticks="2"
        data-stroke-ticks="true"
        data-highlights='[
          {"from": 0, "to": 1000, "color": "rgba(0,255, 0, .3)"},
          {"from": 1001, "to": 2000, "color": "rgba(255, 255, 0, .3)"},
          {"from": 2001, "to": 5000, "color": "rgba(160, 32, 240, .3)"},
          {"from": 5001, "to": 10000, "color": "rgba(255, 0, 0, .3)"}]'
        data-ticks-angle="225"
        data-start-angle="67.5"
        data-color-major-ticks="#ddd"
        data-color-minor-ticks="#ddd"
        data-color-title="#eee"
        data-color-units="#ccc"
        data-color-numbers="#eee"
        data-color-plate="#222"
        data-border-shadow-width="0"
        data-borders="true"
        data-needle-type="arrow"
        data-needle-width="2"
        data-needle-circle-size="7"
        data-needle-circle-outer="true"
        data-needle-circle-inner="false"
        data-animation-duration="1500"
        data-animation-rule="linear"
        data-color-border-outer="#333"
        data-color-border-outer-end="#111"
        data-color-border-middle="#222"
        data-color-border-middle-end="#111"
        data-color-border-inner="#111"
        data-color-border-inner-end="#333"
        data-color-needle-shadow-down="#333"
        data-color-needle-circle-outer="#333"
        data-color-needle-circle-outer-end="#111"
        data-color-needle-circle-inner="#111"
        data-color-needle-circle-inner-end="#222"
        data-value-box-border-radius="0"
        data-color-value-box-rect="#222"
        data-color-value-box-rect-end="#333"
    ></canvas>
  </body>
</html>
