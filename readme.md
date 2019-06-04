# Overview

Script for create raster images of membership cards, visiting cards, certificates, diplomas etc from vector (SVG) template with filling of specified text fields.

# Dependencies

The [Wand](https://pypi.org/project/Wand/) pip package is a wrapper over [ImageMagick](https://en.wikipedia.org/wiki/ImageMagick).
So, ImageMagick should be installed in the system.

# Usage

## Prepare an SVG template

For example, draw it using [Inkscape](https://en.wikipedia.org/wiki/Inkscape), like sample.svg, which is used here.

In SVG file specify desired variables in place of text fields, such as **{{name_family}}**.

```xml
    ...
    ...
    <text
       xml:space="preserve"
       style="font-style:normal;font-weight:normal;font-size:10.58333302px;line-height:1.25;font-family:sans-serif;letter-spacing:0px;word-spacing:0px;fill:#000000;fill-opacity:1;stroke:none;stroke-width:0.26458332"
       x="85.113152"
       y="255.46039"
       id="name_family"
       inkscape:label="#text4815"><tspan
         sodipodi:role="line"
         id="tspan4813"
         x="85.113152"
         y="255.46039"
         style="font-size:8px;text-align:end;text-anchor:end;stroke-width:0.3"
         >{{name_family}}</tspan></text>
    ...
    ...
```

![alt text](sample.svg)


## Call render.py

Bash example:

```bash
python3 render.py -i sample.svg \
    --replacements \
        name_family:"Maria Volkova" \
        list_item_1:"cool web developer" \
        list_item_2:violinist \
        email:masha@mail.ru \
        phone:"+7 987 321 1234" \
    -o sample-result.png
```

For help use:
```bash
python3 render.py -h
```

Example of result:

![alt text](sample-result.png)