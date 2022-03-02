Floorplanning
==========================

This tutorial walks you through using SC's Python-based floorplanning API to
create a full floorplan for the ZeroSoC, a simple system-on-chip meant to
demonstrate SiliconCompiler’s end-to-end design capabilities.

.. image:: _images/zerosoc.png

ZeroSoC is based on a subset of the IP used in the open-source `OpenTitan SoC
<https://github.com/lowrisc/opentitan>`_. It includes:

* An `Ibex <https://github.com/lowrisc/ibex>`_ RV32I processor
* A GPIO controller with 32 configurable I/O ports
* A UART peripheral
* RAM (2KB for ASIC, 8KB for FPGA)

ZeroSoC’s design and supporting files can be found at
https://github.com/siliconcompiler/zerosoc.

Floorplanning methodology
-------------------------
SC includes a library for designing chip floorplans using Python, providing a
high degree of flexibility and easy automation of floorplan design (:ref:`API
Reference<Floorplan API>`). In this tutorial, we describe how to use this API to
iteratively build up a floorplan for ZeroSoC from scratch.  We encourage you to
check your progress using the layout visualizer `KLayout
<https://www.klayout.de/>`_ on each step, an approach that mirrors how you would
develop your own floorplan using this API.

Getting Started
---------------
Before we begin, the first thing to know is that the ZeroSoC ASIC is built in
two parts:

* First, the *core*, which contains the actual digital logic implementing the
  ZeroSoC.
* Second, the *top-level*, which wraps the core and places the ZeroSoC's padring
  (the portion that implements I/O) around it.

We build the ZeroSoC core using SC's included OpenROAD-based flow, and it has
metal pins along its sides for input and output. The core and padring are
designed so that these pins route to the inner pins of the I/O pads by
abutment. Therefore, the top-level does not require automated place and route --
it is defined entirely by the top-level floorplan file. This manual placement is
verified through DRC and LVS, ensuring that it satisfies foundry design rules
and that it matches the Verilog netlist. Understanding this two-part build is
important since we will specify the floorplans of each component separately.

.. figure:: _images/abutment.png

  Note how the pins on the edge of the ZeroSoC core (white background) line up
  with the pins along the edge of the GPIO pads (gray background).

Let's begin by cloning the ZeroSoC Github repository. Be sure to initialize the
submodules to pull down the required third-party design files:

.. code-block:: console

  $ git clone https://github.com/siliconcompiler/zerosoc.git
  $ git submodule update --init --recursive

In order to follow along, you should also :ref:`install
SiliconCompiler<SiliconCompiler Setup>` and the :ref:`KLayout layout
viewer<Tool Setup>`.

If you install SC from PyPI rather than from source, you'll need to clone the
SiliconCompiler repository and configure your SC path to point to the repo in
order to access the included PDK files:

.. code-block:: console

  $ git clone https://github.com/siliconcompiler/siliconcompiler.git
  $ export SCPATH=$PWD/siliconcompiler/siliconcompiler

.. note::
   If you close your shell, you'll need to rerun the ``export`` command from the
   code block above in your next session. To avoid this, you can add the command
   to your ``~/.bashrc`` to have it always apply.

The ZeroSoC repo already includes a completed floorplan, ``floorplan.py``. If
you want to follow along with each step of this tutorial, go ahead and delete or
rename that file and create a blank ``floorplan.py`` in its place. Then, copy in
the following boilerplate::

  from siliconcompiler.core import Chip
  from siliconcompiler.floorplan import Floorplan

  import math

  def configure_chip(design):
    # Minimal chip configuration goes here, for testing

  def core_floorplan(fp):
    # Definition of core floorplan goes here

  def main():
    core_chip = configure_chip('asic_core')
    core_chip.write_manifest('core_manifest.json')
    core_fp = Floorplan(core_chip)
    core_floorplan(core_fp)
    core_fp.write_def('asic_core.def')

  if __name__ == '__main__':
    main()

This file gives us a framework to start designing ZeroSoC's core floorplan. The
``main()`` routine first calls a function ``configure_chip()``, which returns an
SC :class:`~siliconcompiler.core.Chip` object, and uses that to instantiate a
:class:`~siliconcompiler.floorplan.Floorplan` object. The ``Floorplan``
constructor requires a ``Chip`` object since aspects of the floorplan are
defined based on the chip configuration.  We'll point out examples of this
throughout the tutorial.

Next, ``main()`` calls ``core_floorplan()``, which will ultimately use the
functions provided by the floorplan API to generate the floorplan itself.
Finally, ``main()`` calls a method of the floorplan object, ``write_def()``, to
generate an output DEF file that we can either preview in KLayout or pass into
an SC compilaton flow.

Minimal chip configuration
------------------------------
The first thing we need to do to is fill out our ``configure_chip()`` function
with a minimal configuration. Floorplanning relies on the following items being
configured in the provided chip object:

1) A technology target, for providing technology-specific information.
2) A design name, used to name the layout in the output file.
3) Macro libraries, in order to perform macro placement.

Let's fill out ``configure_chip()`` to accomplish these tasks one-by-one. First,
we instantiate a new chip and set its target to Skywater 130, an open-source PDK
that has a demo build target bundled with SC::

..@include configure_chip_target

Next, we'll provide the design name as a parameter so that we can reuse this
configuration function for testing both the core and top padring::

..@include configure_chip_design

Last, we want to configure two macro libraries, one for ZeroSoC's RAM and the
other for ZeroSoC's I/O cells.  The first step to including macros in a design
is to point SC to the relevant files in your build configuration. At a minimum,
you’ll need LEF, GDS, and liberty files for each of your libraries. In the
configuration schema, all macro library configurations live under a key path
starting with ``library``, followed by a designer-defined macro library name.
The following lines show how the ZeroSoC configuration points to its RAM macro
library::

..@include configure_chip_macro

In addition, the name of the macro library must be added to the ``'asic', 'macrolib'``
parameter::

..@include configure_chip_macrolib

Finally, it's a good idea to specify the "type" of a macro library in order to
distinguish it from the technology target-defined standard cell library used for
automated place and route. The standard type for a macro library is
"component"::

..@include configure_chip_type

Note that if you’d like to include a Verilog behavioral model of a macro, that
can be passed to SC just like any other Verilog source. However, keep in mind
that Yosys creates a blackbox definition of all cells defined in liberty files
it reads, and if it reads a  Verilog source that defines the same module, this
will trigger an error. Therefore, to switch between a behavioral model and a
blackbox, we recommend creating a wrapper that instantiates one or the other
based on a parameter or preprocessor macro. Since we don't need Verilog sources
for our minimal configuration, this isn't shown here.

With all these pieces included, along with additional configuration for the I/O
library, your definition of ``configure_chip()`` should look like this::

..@include configure_chip

Note we've also added a few lines to set up the chip's ``showtool`` parameter.
While this isn't part of the minimal configuration required for using the
floorplan API, it is required to use ``sc-show``, a tool we'll use to preview
your floorplan later on in the tutorial. This will usually be handled for you by
SC's built-in flows, but we need to do it ourselves here since we don't have a
flow target for this minimal config.

Before moving on, we'll also define some constants above ``configure_chip()`` in
order to concisely reference the names of each macro we plan to use::

..@include macro_names


Chip dimensions
----------------
The first step to floorplanning a chip is to define the actual size and
placement area of the chip itself. Since ZeroSoC is implemented as a multi-step
build, we'll define these dimensions in a new function that can be reused by
both the core and top-level floorplan, so that we don't have any integration
bugs due to dimension mismatch. Let's call this function
``define_dimensions()``, and have it take in a floorplan object called ``fp``.
You can place this function right after ``configure_chip()``::

..@include define_dimensions_prototype

First, let's define two variables that specify the size of the area in the
middle of the chip where automated place and route can put standard cells, as
well as two variables that specify the size of the bottom and left margins
around this area. The power delivery rings will go in this margin::

..@include place_dims

Note that these dimensions are calculated based on two values extracted from the
``fp`` object: the standard cell width and standard cell height. Making sure the
margins are multiples of the standard cell size ensures that routing tracks and
standard cell placement are aligned properly for the automated place and route
tool to easily route to each cell. This is an example of why we need to provide
a configured ``Chip`` object to instantiate our ``Floorplan`` object -- that's
how it extracts this information.

Based on these margins and placement area, we can compute the size of the core
itself::

..@include core

Although we're not going to use it right away, we next compute the size of the
ZeroSoC top-level, which must be equal to the core plus the height of the
padring along each edge::

..@include top

Our padring height is going to be equal to the height of our I/O library's GPIO
cell. The floorplan API provides us with the ability to look up the dimensions
of macros through its ``available_cells`` dictionary.

We also wrap this calculation in ``math.ceil()`` to round these dimensions up to
a whole number of microns. Having these dimensions be whole numbers is necessary
for us to construct the padring, which we'll discuss later on in the tutorial.

Since we round up the top-level dimensions a bit, as a final step we need to
adjust our core dimensions to compensate. This implicitly stretches the
top and right margins to ensure that all of our alignment constraints are met::

..@include core_stretch

Putting this all together along with a return statement to provide all the
important dimensions from this function to the caller, we get::

..@include define_dimensions

Specifying die area
-------------------
Now that we have the basic size of our chip defined, we can begin to define
ZeroSoC's core floorplan. To initialize a floorplan, we first need to call
:meth:`~siliconcompiler.floorplan.Floorplan.create_diearea()` on our floorplan
object, passing in the relevant dimensions. Put the following code in
``core_floorplan()``::

..@include die_area

The first argument to ``create_diearea`` specifies the overall size of the chip,
provided as a list containing the coordinates of the bottom-left and top-right
corners, respectively (the bottom-left is generally ``(0, 0)``).  The
``corearea`` keyword argument takes input in the same form and specifies the
legal area for placing standard cells (note that the term "core" in ``corearea``
refers to something other than the ZeroSoC "core").

With this call, we now have a minimal SC floorplan! To preview your work, go
ahead and run ``floorplan.py``. This should produce some log output, as well as
2 files: ``asic_core.def`` and ``core_manifest.json``. The ``.def`` file contains
our floorplan in DEF format, while ``core_manifest.json`` contains our chip
configuration in SiliconCompiler’s JSON manifest format. We can display this DEF
file in KLayout by running the following command:

.. code-block:: console

  $ sc-show -read_def "show 0 asic_core.def" -cfg core_manifest.json

``sc-show`` uses the information in ``core_manifest.json`` to configure KLayout
according to our technology and macro library specifications to give you a
proper view of your DEF file. KLayout should open up and show you an outline of
the core, like in the following image.

.. image:: _images/die_area.png

Placing RAM
-----------
An orange rectangle isn't very exciting, so let's spruce things up by placing
the RAM macro. We'll do this using the floorplan API's
:meth:`~siliconcompiler.floorplan.Floorplan.place_macros` function, which allows
you to place a list of macros from a starting position and a given pitch along
the x and y-axes. To place a single macro like the ZeroSoC’s RAM, we'll just
pass in a list of one instance, and 0s for the pitch values. Note that we
specify ``snap=True`` to ensure the RAM's position is standard-cell aligned.
This ensures proper alignment for routing.  Insert the following code after our
call to ``create_diearea()``::

..@include ram_placement

We use our predefined dimensions as well as the RAM size information stored in
``available_cells`` to place the macro in the upper-right corner of the design.
We place it here because most of the pins we need to access are on the left and
bottom of the macro, and this ensures those pins are easily accessible. We lower
its height by a bit to make space for the router to tie-off a couple pins on the
other sides of the macro.

It's important to pay attention to how macro instances are specified. Each
macro is specified as a tuple of two strings: the first is the particular
instance name in the design, and the second is the name of the macro itself.
Getting this instance name correct (accounting for the flattened hierarchy,
indexing into generate blocks, etc.) can be tricky, and it’s important to get it
right for the macro placement to be honored by design tools. The following
naming rules apply for the Yosys synthesis tool in particular:

* When the hierarchy is flattened, instance names include the instance names
  of all parent modules separated by a ``.``.
* Generate blocks are included in this hierarchy. We recommend naming all
  generate blocks, since they'll otherwise be assigned a name generated by
  Yosys.
* When a generate for-loop is used, an index is placed after the name of the
  block, in between square brackets. The square brackets must be escaped with
  ``\\`` in Python code, in order to escape it with a single ``\`` in the DEF
  file.

Examples:

* ``soc.ram.u_mem.gen_sky130.u_impl_sky130.gen32x512.mem``
* ``padring.we_pads\\[0\\].i0.padio\\[5\\].i0.gpio``

Along with the macro placement itself, we use
:meth:`~siliconcompiler.floorplan.Floorplan.place_blockage` to define a
placement blockage layer to ensure that standard cells aren't placed too close
to the RAM pins, which can result in routing congestion::

..@include blockage_placement

Now, if we run ``floorplan.py`` and view the resulting DEF, we can see the RAM
macro placed in the top right of the die area, with the blockage area besides
and below it highlighted.

.. image:: _images/ram.png

Placing Pins
------------
To complete the core, we need to place pins around the edges of the block in the
right places to ensure these pins contact the I/O pad control signals. Just like
with the chip dimensions, we need to share data between both levels of the
ZeroSoC hierarchy here, so we'll specify these dimensions in a new common Python
function. We'll call this function ``define_io_placement()``, and start off by
defining four lists with the order of the I/O pad types on each side::

..@include iolist

We want to design the floorplan so that the pad cells are evenly spaced along the
west and south sides of the chip, and evenly spaced in two groups on the north
and east sides. We could calculate the positions by hand, but since we're using
Python, we can do it programatically instead!

First, we'll define a helper function called ``calculate_even_spacing()``::

..@include calculate_even_spacing

This function takes in a list of padcell names, does some math to calculate the
required spacing between cells, and then returns a new list, pairing each entry
with the position of that padcell.

Putting this all together, we can make use of this helper function to give us
what we want::

..@include define_io_placement

Now, back to the pins! Since there are actually multiple control signals for
each GPIO pad, we first construct a list that contains the name of each one,
their offset in microns from the edge of the pad, and some additional info
needed to handle indexing into vectors. We also define some values that are the
same for every pin we place. Add the following below the ``fp.place_blockage()``
call in ``core_floorplan()``::

..@include pin_data

Now we can write two nested for-loops for each side, the first over the list of
pad positions, and the second over the pin offsets, to calculate the position of
each pin. We place the pins using
:meth:`~siliconcompiler.floorplan.Floorplan.place_pins`. Here's the code for placing
all four sides, with the logic in the first loop annotated with comments::

..@include pin_loops

If we build the core DEF now, and zoom in closely to one side of the die, we
should see the same clustered pattern of pins spaced out along it.

.. image:: _images/pins.png

PDN
---
The last important aspect of the core floorplan is the PDN, or power delivery
network.  Since this piece is relatively complicated, we'll create a new
function, ``place_pdn()``, that encapsulates all the PDN generation logic::

..@include place_pdn_def

We'll also add a call to this function at the bottom of ``core_floorplan()``::

..@include place_pdn_call

``place_pdn()`` takes in the floorplan to modify, as well as the RAM macro's
position and margin. These additional values are important to ensure the PDN
doesn't accidentally short anything in the RAM macro. We also call our helper
functions to get the other relevant dimensions of our design.

The goal of the power delivery network is to create a grid over our entire
design that connects VDD and GND from our I/O pads to each standard cell, as
well as the RAM macro. This grid consists of horizontal and vertical straps, and
we'll add some variables to our function to parameterize how these straps are
created. Then, we'll use these parameters to calculate an even pitch for the
grid in both directions::

..@include pdn_config

Note that we don't calculate ``vpitch`` across the entire distance of the chip:
the vertical straps don't cross the RAM macro, since the macro includes wiring
on metal layer 4, and this could cause a short.

The first thing we have to do before we can define any of the actual objects in
our PDN is to add the definitions of the two "special nets" that are associated
with our power signals.  We do this with
:meth:`~siliconcompiler.floorplan.Floorplan.add_net`::

..@include pdn_add_nets

We have one call for our power net, and one call for our ground net. The first
parameter gives the name of the net in our Verilog design, while the second
parameter is a list of pin names that should be connected to that net (in our
case, "VPWR" and "VGND" for the standard cells, and "vccd1" and "vssd1" for the RAM
macro).  Finally, the last parameter gives the type of net, based on a set of
labels defined in the DEF standard. In our case, "_vdd" is of type "power" and
"_vss" is of type "ground."

With this configuration done, any calls to the floorplan API relating to our
power nets can refer to either the "_vdd" net or the "_vss" net by name.

The first pieces of PDN geometry we'll set up are the power and ground rings
that circle the design. These rings form the interface between the power signals
coming from our padring and the power grid that distributes those signals. To
instantiate the rings, we'll do some math to calculate their dimensions, and
then call :meth:`~siliconcompiler.floorplan.Floorplan.place_ring` to create
them::

..@include pdn_place_ring

If you regenerate the DEF file, you can now see two rings of wires circling the
ZeroSoC core.

.. image:: _images/pdn_ring.png

Next, we'll place the straps that form the power grid itself. These stretch from
one end of the ring to the other, and alternate power and ground. We place these
by calling :meth:`~siliconcompiler.floorplan.Floorplan.place_wires`, and we'll
duplicate the net name in the first argument and use the pitch parameter to
place multiple straps with each call::

..@include pdn_power_straps

Rebuild the floorplan and you should see a result like this:

.. image:: _images/power_straps.png

Now, we need a way to deliver power from the padring to the power rings. To do
so, we'll add a few pieces of metal that will abut the correct ports on the
power padcells, and overlap the corresponding wires in the ring. We do this with
a few for-loops over the pads::

..@include power_pad_connections

We use ``place_pins()`` here since these wires are all associated with the
top-level power pins of the core. However, for the VDD and VSS pads we also have
to make a call to ``place_wires()`` overlapping these pins for two reasons:

1. Via generation (covered later) only looks at special nets, and we need to
   ensure that there are vias inserted between these pins and the power ring
   (since they're on different layers).
2. Some automated place and route tools such as OpenROAD can't handle pins that
   extend beyond the design's boundaries, but we need the pads to extend further
   to account for the difference in height between the GPIO and power padcells.
   This is why ``pow_gap`` is used in the dimension calculations for the wires,
   but not the pins.

The VDDIO pins don't need an overlapping special net because VDDIO is routed to
GPIO pin tie-offs automatically by the signal router.

With these wires added, you should see something like the following along each
side of your design:

.. image:: _images/power_pins.png

There are now two steps left to finishing up the PDN. First, we need to connect
together all overlapping wires that are part of the same net. Next, we need to
connect these wires to the wires that supply power to the standard cells, as
well as the pins that supply power to the RAM macro.

In order to accomplish both these tasks, we'll need to insert vias in the
design. The floorplan API has a useful helper function that will insert vias
between all common nets on specified layers. However, before we call this
function, we're going to add a few more wires that will enable us to set up all
the power connections to the design itself.

The standard cells are automatically placed in rows with alternating power and
ground stripes on metal layer 1. We can power them by placing wires over these
stripes, and connecting vias to these wires. We perform some calculations based
on the standard cell info in the floorplan object in order to determine the
positions of these stripes, and then place them::

..@include stdcell_straps

Note that we have to be careful not to place these over the RAM macro, which
interrupts the standard cell placement in the top-right corner. We handle this
by placing the stripes in two groups, the bottom ones taking up the full width
of the core and the top ones only going until the RAM macro. We also set the
"followpin" attribute on these wires, which indicates to our design tool that
they are overlapping the power pins of cells in the design.

Next, we place some wires over the RAM macro's power pins::

..@include ram_power_pins

Once these are all set up, we can now insert vias between wires by calling
:meth:`~siliconcompiler.floorplan.Floorplan.insert_vias`::

..@include insert_vias

The ``layers`` argument to this function takes in a list of pairs of layer
names, describing which pairs should be connected with vias. In our case, we
need to connect ``m1`` and ``m4`` to power the standard cells, ``m3`` to ``m4``
and ``m5`` to connect the power pins to the rings, and ``m4`` and ``m5`` to
connect the grid wires together as well as power the RAM macro.

The final floorplan should look like the following. All the blue lines are the
dense metal 1 stripes providing power to each standard cell.

.. image:: _images/complete_pdn.png

If you zoom in closer, you should be able to see the vias inserted in various
places:

.. image:: _images/vias.png

Top-level padring
------------------
Now that we've completed floorplanning the core, it's time to put together the
padring and complete the picture! Since we've laid a lot of the groundwork
already via our common functions, this shouldn't take quite as much code.

However, before we can work on the padring, we need to add a bit more to our
boilerplate. First, we'll add a new function within which we'll define the
top-level floorplan::

  def top_floorplan(fp):
    # Design top-level floorplan here...

We'll also add some code to ``main()`` to let us test it::

  def main():
    chip = configure_chip('asic_core')
    chip.write_manifest('core_manifest.json')
    fp = Floorplan(chip)
    core_floorplan(fp)
    fp.write_def('asic_core.def')
    fp.write_lef('asic_core.lef') # NEW

    # NEW:
    chip = configure_chip('asic_top')

    # Add asic_core as library
    libname = 'asic_core'
    chip.add('asic', 'macrolib', libname)
    chip.set('library', libname, 'type', 'component')
    chip.set('library', libname, 'lef', 'asic_core.lef')

    chip.write_manifest('top_manifest.json')

    fp = Floorplan(chip)
    top_floorplan(fp)
    fp.write_def('asic_top.def')

There are several differences here between our old boilerplate and the new.
First, we add a line to write out an abstracted LEF file of the core. This is
because we need to incorporate the core as a library that will be used within
the top-level. We also have to include a few lines of additional chip
configuration to set up this library, just like we did for the RAM and I/O.

With the setup completed, we can work on designing the padring itself. Our main
task is to place the proper type of I/O pad at its corresponding location
specified in ``define_io_placement()``. We can do this by looping over the list
and using :meth:`~siliconcompiler.floorplan.Floorplan.place_macros`, much like
how we placed the pins in the core (but without having to worry about pin
offsets)::

..@include place_pads_loop

Note that for layout-versus-schematic verification, our top-level floorplan
needs to have pins defined that correspond to the top-level I/O of the Verilog
module. Since our module's ports correspond to the pads on the padring cells, we
place pins directly underneath these pads, shorted to the pads by being placed
on the same layer (in this case, metal 5).

Now, if we build this and open ``asic_top.def``, you should see I/O macros
spaced out along each side, with the ordering of GPIO versus power pads
corresponding to the lists defined earlier.

.. image:: _images/unfilled_padring.png

One other thing we need to do is insert wires connecting the VDDIO power pads to
the pins on the core. We can accomplish this with another set of four loops over
the pads on each side::

..@include place_vddio_pins

Next, we need to fill in the padring in order to allow power to be routed
throughout it. First, we'll place corner cells on each of the four corners,
using another set of ``place_macros()`` calls::

..@include place_macros

Note that the corner cells aren't represented in our Verilog netlist (since they
are just dummy metal cells that don't implement any logic), so we don't have to
worry about the instance names here.

Since our pads have gaps between them, we also need to insert I/O filler cells
to complete the padring. In order to save you the effort of manually specifying
the location of these cells, the floorplan API provides a function
:meth:`~siliconcompiler.floorplan.Floorplan.fill_io_region` to do this
automatically. This function takes in a region and a list of I/O fill cells, and
places fill cells inside the empty space in the region. To complete the ring, we
call this function four times, once for each of the four sides::

..@include fill_io

Looking at the padring now, we can see that it is a complete ring!

.. image:: _images/padring.png

If you zoom in one part of the padring you should see that the metal wires cutting
through the fill cells are aligned with pins on each side of the corner and pad
cells:

.. image:: _images/ring_complete.png

Finally, to implement the full ZeroSoC hierarchy, we place the core as a macro
inside the padring::

..@include place_core

We can now generate our final top-level floorplan, and zoom in on the interface
between a padcell and the core to make sure the I/O aligns correctly:

.. image:: _images/pins_connect.png

Note that the wires extending beyond the core boundary to connect the power pad
cells won't be visible, since special nets are not included in the abstracted
LEF view.

Here's the completed function for building the ZeroSoC top-level::

..@include top_floorplan

Congratulations! You've successfully floorplanned an entire SoC using Python and
SiliconCompiler.

Building ZeroSoC
--------------------

To see your floorplan in action, you can go ahead and build ZeroSoC with the
following command:

.. code-block:: bash

  $ python build.py

Note that this requires installing all the EDA tools used by SC's SystemVerilog
ASIC flow.

This will put together the entire ZeroSoC hierarchy and run DRC/LVS
verification. The final result will be found in
``<build_dir>/asic_top/job0/export/0/outputs/asic_top.gds``.
