#@ OpService ops
#@ ImgPlus img
#@ ImgPlus kernel
#@OUTPUT ImgPlus convolved
#@OUTPUT ImgPlus deconvolved

from net.imglib2 import Point
from net.imglib2.algorithm.region.hypersphere import HyperSphere
from net.imglib2.util import Intervals

# crop PSF to desired size, this makes conv and decon run faster with little effect on final quality
croppedX=64;
croppedY=64;

kernelX = kernel.dimension(0)
kernelY = kernel.dimension(1)
kernelZ = kernel.dimension(2)

kernel_=ops.transform().crop(kernel, Intervals.createMinMax(kernelX/2-croppedX/2, kernelY/2-croppedY/2, 0,
	kernelX/2+croppedX/2-1, kernelY/2+croppedY/2-1, kernelZ-1))

# convolve kernel with phantom
convolved=ops.filter().convolve(img, kernel)

# make convolved an ImgPlus
convolved=ops.create().imgPlus(convolved);
convolved.setName("convolved")

deconvolved = ops.create().img(convolved);
deconvolved = ops.deconvolve().richardsonLucy(deconvolved, convolved, kernel, [0,0,0], None,
					None, None, None, 30, True, True);

