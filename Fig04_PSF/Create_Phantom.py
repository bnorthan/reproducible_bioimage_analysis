#@ OpService ops
#@OUTPUT ImgPlus(label="Phantom") phantom

# This script creates a phantom that consists of a hyperSphere in the center
#
# 1.  Draw a sphere on a 256, 256 by 256 image 
# 2.  Rescale by 0.4 in Z to simulate the common case where voxel depth is greater then x and y

from net.imglib2 import Point
from net.imglib2.algorithm.region.hypersphere import HyperSphere
from net.imglib2.util import Intervals
from net.imglib2.realtransform import AffineTransform3D
from net.imglib2.interpolation.randomaccess import NLinearInterpolatorFactory
from net.imglib2.view import Views;
from net.imglib2.util import Intervals
from net.imglib2.realtransform import RealViews;

xSize=256;
ySize=256;
zSize=256;

# create an empty image
phantom=ops.create().img([xSize, ySize, zSize])

# make phantom an ImgPlus
phantom=ops.create().imgPlus(phantom);

location = Point(phantom.numDimensions())
location.setPosition([xSize/2, ySize/2, zSize/2])

hyperSphere = HyperSphere(phantom, location, 10)

for value in hyperSphere:
        value.setReal(100)

phantom.setName("phantom")

affine = AffineTransform3D();
affine.scale(1, 1, 0.4);

interpolatedImg = Views.interpolate(Views.extendZero(phantom), NLinearInterpolatorFactory());
 
phantom = Views.interval(Views.raster(RealViews.affine(interpolatedImg, affine)),Intervals.createMinMax(0,0,18,255,255,82));

# make phantom an ImgPlus
phantom=ops.create().imgPlus(ops.copy().iterableInterval(Views.zeroMin(phantom)))
phantom.setName('phantom');