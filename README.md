3D Lindenmayer System Tree (in Blender)
=======================================

What is this?
-------------
This is a very simple example of how to use Lindenmayer Systems (a.k.a.
L-Systems) to generate a fractal tree in Blender.


Examples
--------
![A Simple Tree](https://gitlab.com/define-private-public/3D_L-System_Tree/raw/master/examples/basic-tree.png)

![A More Natural Tree](https://gitlab.com/define-private-public/3D_L-System_Tree/raw/master/examples/random-tree.png)


How-To Use
----------
Open up a new instance of Blender and change to the "Scripting," view.  In the
script editor panel, open up the `./l-system_tree.py` file.  Make any tweaks
that you want and then press `Run Script`.  The base of the tree will where the
3D cursor currently is.

At the top of the script, there are some configuration varaibles that you can
change to alter the tree that is generated.  Try turning on `VARIATION_MODE`; it
generates more natural looking trees.


License
-------
It's a 3-Clause BSD.  Check the file `./LICENSE` for details.

