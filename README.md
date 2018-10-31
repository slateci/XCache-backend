# XCache network 

A simple node.js server that:

a) manages xrootd federation
* once per minute looks up XCache infrastructure from ES 
* creates lookup tables for every XCache.
* for a given client site and filename returns optimal path.
b) simulates a federation

c) creates stress infrastructure.

## To Do:
* XCache servers to report status through the backend to ES
* current calculation is based on equal capacity servers. Which won't always be the case.
* each cache record contains info on one server: 
**	cache it belongs to
**  sites it serves
**  upstream sites (list of two)
**  cache coordinates
**  status
**  index in cache
**  capacity (disk size * HWM)
