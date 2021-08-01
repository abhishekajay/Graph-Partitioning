=============================================
	description 
==============================================

(1). Experiments are being done on random graphs of sizes 20,30,...200. The graphs given as  input to the algorithm are stored as csv file with format node1,node2,weight.
(2). Data files for each node are stored in the ./node/data/ for eg: Graphs for 20node graphs are stored in ./20nodes/data/   
(3). The heuristic algorithm uses the joblib package for parallelisation and one can disable it by setting nproc in ./codes/algo.py line 287 to 1 
(3). Results of each experiment is stored in the corresponding result directory as an .html file. for eg: results of case study of 20node erdos-reyni random graph is stored in  ./20nodes/result/ as 20nodesp=0.5.html  
(4). If you want to test the algorithm on a particular graph for eg: graph.csv with the format of graph.csv as given above in step 1, use the cammand python3 Runner.py graph.csv then output will be fiedler values of heuristic, kernighan-Lin and spectral bisection algorithms. 
(5). Order of complexity figure and profiling results are present in ./codes/


References:
[1]. Schulz C. 2013 High quality graph partitioning.PhD thesis, Karl-
sruhe Institute of Technology, karlsruhe, German

[2]. B. W. Kernighan and S. Lin, “An Efficient Heuristic Procedure
for Partitioning Graphs,” Bell System Technical Journal, vol. 49, no.
2, pp. 291–307, 1970

[3]. Aric A. Hagberg, Daniel A. Schult and Pieter J. Swart, “Exploring
network structure, dynamics, and function using NetworkX”, in Pro-
ceedings of the 7th Python in Science Conference (SciPy2008), Gäel
Varoquaux, Travis Vaught, and Jarrod Millman (Eds), (Pasadena,
CA USA), pp. 11–15, Aug 2008

[4]. Joblib, “joblib/joblib,” GitHub. [Online].
Available: https://github.com/joblib/joblib

[5].https://github.com/rkern/line_profile

If you find this repository useful in your work, we request you to cite the following paper [https://www.sciencedirect.com/science/article/pii/S1476945X21000416]:

@article{kumar2021stability,
  title={Stability aware spatial cut of metapopulations ecological networks},
  author={Kumar, Dinesh and Ajayakumar, Abhishek and Raha, Soumyendu},
  journal={Ecological Complexity},
  volume={47},
  pages={100948},
  year={2021},
  publisher={Elsevier}
}