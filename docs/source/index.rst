.. pythogram-core documentation master file, created by
   sphinx-quickstart on Mon Aug 27 10:46:00 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Pythogram-core documentation
============================

Contents:

.. toctree::
   :maxdepth: 2

   developer_guide
   api_reference
   testing_reference

   
Refactoring
-----------

Internal format should be kept to numpy.array wherever possible. The new structure will be as follows:

* gramcore
   * datasets
      * images - tile/prepare_synth, synth, noise
      * polygons - orthogonals
      * surfaces - dtm, dsm, noise
      * masks - are these still relevant?
      * changes - ??
   * operations
      * images - load, save, split, resize, rotate, fromarray
      * arrays - load, save, split, asarray
      * polygons - scale, rotate, move, export
   * features, or just features without the rest
      * edges - prewitt, sobel, canny
      * thresholding - ??
      * points - harris, hog
      * statistics - min, max, mean, average etc
      * morphology - grey_ersosion etc
      * indexes - ndvi
      * selection ???
   * classification
      * svm