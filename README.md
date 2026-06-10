# Sprint 2

## By Makani Buckley

## Introduction

For Sprint 2, I aimed to fix 2-4 bugs in the VisIt repository. In particular, I
created solutions for Bugs \#20955, \#4999, and \#17574 and found no issues for
Bugs \#4976 and \#5213. I also looked at Bug \#5618 but was blocked by available
hardware. In the following sections, I will describe each bug and how I worked
with it. The project is available [here](https://github.com/makanicb/CS410-SciVis_Sprint2).

## Bug \#20955

[Link to Issue](https://github.com/visit-dav/visit/issues/20955)

### Issue

For SILO files containing null material names, VisIt would not register the
existence of the null-named materials.

To recreate the issue, run `bug20955.py`
on ix-dev. The data for this test was retrieved from [here](https://github.com/llnl/conduit/tree/develop/src/tests/relay/data/silo/overlink).

In particular, the data in
`src/tests/relay/data/silo/overlink/overlinkMatColorsNullMatnames/` was used.
The directory contains two files `OvlTop.silo` and `domain0.silo`. For these
tests, `domain0.silo` needed to be placed in a subdirectory of
`overlinkMatColorsNullMatnames/` with the same name. The resulting directory
structure is:
```
overlinkMatColorsNullMatnames
├── overlinkMatColorsNullMatnames
│   └── domain0.silo
└── OvlTop.silo
```

The data in these files consists of a 2x2 cell rectilinear grid spanning (0,0)
to (2,2) with two materials named "Good" and NULL. The "Good" material covered
the left 2 cells, and the NULL material covered the right two cells.

When running `bug20955.py` observer that both materials are registered in the
metadata of the FilledBoundary plot and the SILO database, but the spatial
extents of the plot span only from (0,0) to (1,2), i.e. only the "Good" material
is being rendered. If running VisIt on a system with the ability to render
windows, unlike ix-dev, drawing the FilledBoundary plot also shows that only the
"Good" material is being drawn.

### Fix

The fix to this issue can be found in `avtSiloFileFormat.C`. In particular,
while the SILO database reader did have logic for reading materials with NULL
names for metadata (in functions like `avtSiloFileFormat::ReadMaterials()`),
this logic was missing when the reader went to use the material. Specifically,
`avtSiloFileFormat::CalcMaterial()`, which takes the SILO database and returns
and returns an `avtMaterial` object, did not have the logic for handling NULL
material names. Adding in this logic fixes the issue. 

To recreate the fix, copy `avtSiloFileFormat.C` to
`visit3.4.0/src/databases/Silo/avtSiloFileFormat.C` using a command such as  
```$ cp /home/users/makanib/uoregon-cs410-scivis/sprint2/avtSiloFileFormat.C visit3.4.0/src/databases/Silo/avtSiloFileFormat.C```

## Bug \#4999

[Link to Issue](https://github.com/visit-dav/visit/issues/4999)

### Issue

In .visit files, the `!TIME` keyword was not being honored to set time values
for the database. 

To recreate the issue, run `bug4999.py` on ix-dev. The data used for this test
is found in the original issue as
[KelvinHelmholtz.zip](https://github.com/visit-dav/visit/files/5120164/KelvinHelmholtz.zip).

The data consists of a .visit file using the `!TIME` keyword to set the time for
three VTK data sets. Specifically, these times were `0.0`, `0.7012092338664179`,
and `1.5`.

However, when running `bug4999.py` observe that the time values reported for the
three time steps do not match these `!TIME` values. 

### Fix

In the source code for VisIt, the responsibility for reading .visit files exists
in `avtDatabaseFactory.C` under `avtDatabaseFactory::VisitFile()`. This function
calls `avtDatabase::GetFileListFromTextFile()` to retrieve the list of data
files and `avtDatabaseFactory::FileList` to generate an `avtDatabase` from them.
Both of these functions expect that `!` keywords will be included in the file
list, but there is a contradiction in how the `!NBLOCKS`, `!TIME`, and
`!ENSEMBLE` keywords are handled. Specifically, `avtDatabaseFactory::FileList()`
expects to receive these keywords in the file list so that it can process them
while generating the database, but `avtDatabase::GetFileListFromTextFile()`
skips them and excludes them from the file list it returns.
`avtDatabase::GetFileListFromTextFile()` does handle the processing of
`!NBLOCKS` but it ignores `!TIME` and `!ENSEMBLE`. 

My solution was to modify `avtDatabase::GetFileListFromTextFile()` in
`avtDatabase.C` so that it does not skip the `!TIME` and `!ENSEMBLE` flags
allowing them to be processed by `avtDatabaseFactory::FileList()`. I also
observed in `avtDatabaseFactory::FileList()` that `!` keywords are expected to
all precede file names in the file list. Thus, I also modified
`avtDatabase::GetFileListFromTextFile()` to sort `!` keywords to the start of
the file list (while maintaining the ordering of keywords and filenames
respectively).

Recreate this fix by copying `avtDatabase.C` to
`visit3.4.0/src/avt/Database/Database/avtDatabase.C` via a command like  
```$ cp /home/users/makanib/uoregon-cs410-scivis/sprint2/avtDatabase.C visit3.4.0/src/avt/Database/Database/avtDatabase.C```

I do have some concerns about this solution. I do not like how it directly
contradicts the changes to `avtDatabase.C` which specifically skip `!NBLOCKS`,
`!TIME`, and `!ENSEMBLE`. It seems like this change was part of a shift to move
the processing of keywords out of `avtDatabaseFactory::FileList()`, but it
appears this shift may not have been carried all the way through. I worry that
other functions and files may have been altered during this shift and that
changing the code to not skip `!TIME` and `!ENSEMBLE` will break other parts of
the code I am unfamiliar with. I am also unsure if sorting keywords to the start
of the file list is the right move, or if users should be expected to handle
this convention themselves.

## Bug \#17574

[Link to Issue](https://github.com/visit-dav/visit/issues/17574)

### Issue

While initializing a DBOptionsAttributes object, calling `SetEnumStrings` before
`SetEnum` causes VisIt to crash.

Recreate this bug by copying `testDBOptionsCrash.C` to
`visit3.4.0/src/common/state/` by doing  
```cp /home/users/makanib/uoregon-cs410-scivis/sprint2/testDBOptionsCrash.C visit3.4.0/src/common/state/```  
Then append the lines  
```
ADD_EXECUTABLE(testDBOptionsCrash testDBOptionsCrash.C)  
TARGET_LINK_LIBRARIES(testDBOptionsCrash visitcommon)
```  
to the end of `visit3.4.0/src/common/state/CMakeLists.txt` via  
```
$ echo "ADD_EXECUTABLE(testDBOptionsCrash testDBOptionsCrash.C)" >> visit3.4.0/src/common/state/CMakeLists.txt  
$ echo "TARGET_LINK_LIBRARIES(testDBOptionsCrash visitcommon)" >> visit3.4.0/src/common/state/CMakeLists.txt
```  
Then `make` your changes by going to `visit3.4.0/build` and running  
`$ make testDBOptionsCrash`  
Finally, run `visit3.4.0/build/exe/testDBOptionsCrash` to recreate the bug.

When running `visit3.4.0/build/exe/testDBOptionsCrash` observe that VisIt does
crash.

### Fix

The crash described by the issue occurs because VisIt throws an exception in
`DBOptionsAttributes::SetEnumStrings()` when the function is called on an
enumerated type which has not yet been initialized using
`DBOptionsAttributes::SetEnum()`.

This is reasonable behavior, but, as the issue suggests, I modify the code to
instead output a warning and then initialize the new enumerated type itself.

You may recreate the fix by copying `DBOptionsAttributes.C` to 
`visit3.4.0/src/common/state/DBOptionsAttributes.C` via  
```$ cp /home/users/makanib/uoregon-cs410-scivis/sprint2/DBOptionsAttributes.C visit3.4.0/src/common/state/DBOptionsAttributes.C```

I do have some reservations about this solution. Namely, I am not convinced that
it is better to warn in this case rather than throw an exception. I do assume
in this solution that 0 is a good default value for the new type. Moreover,
the warning is currently output to `cerr`, but I believe some `debug [1-5]` may
be more appropriate in VisIt's context.

## Bug \#4976

[Link to Issue](https://github.com/visit-dav/visit/issues/4976)

### Issue

When revolving a 2D curvilinear multi-mesh, VisIt crashes. 

Recreate this issue by running `bug4976.py`. The data used in this test is part
of the [VisIt Data Files](https://visit-dav.github.io/largedata/datarchives/visit_data_files),
particularly, `visit_data_files/multi_curv2d.silo`.

Observe that, when running `bug4976.py`, VisIt does not crash. This is despite
the script following the exact steps described in the issue.

I followed up on the original thread to see if the bug is still an issue.

## Bug \#5213

[Link to Issue](https://github.com/visit-dav/visit/issues/5213)

### Issue

Within the `ViewerPlot` class the fields `fgColor` and `bgColor` are not
properly updated when the foreground and background colors of the window are
updated.

To recreate the issue, copy `ViewerPlot_w_cerr.C`, `ViewerPlotList_w_cerr.C`,
and `ViewerWindow_w_cerr.C` into the VisIt source via  
```
$ cp /home/users/makanib/uoregon-cs410-scivis/sprint2/ViewerPlot_w_cerr.C visit3.4.0/src/viewer/core/ViewerPlot.C  
$ cp /home/users/makanib/uoregon-cs410-scivis/sprint2/ViewerPlotList_w_cerr.C visit3.4.0/src/viewer/core/ViewerPlotList.C  
$ cp /home/users/makanib/uoregon-cs410-scivis/sprint2/ViewerWindow_w_cerr.C visit3.4.0/src/viewer/core/ViewerWindow.C
```  
Then run `make` inside `visit3.4.0/build/viewer/core/`. Finally, run
`bug5213.py` using VisIt.

When running `bug5213.py` observe that when `ViewerPlot::SetForegroundColor()`
or `ViewerPlot::SetBackgroundColor()` are called, the foreground and background
color maintained in `fgColor` and `bgColor` are updated.

Thus, it appears the the issue has been resolved. I followed up on the original
thread to confirm that this is the case.

## Bug \#5618

[Link to Issue](https://github.com/visit-dav/visit/issues/5618)

### Issue 

`avtRectilinearDomainBoundaries::ExchangeMesh` appears to be faking coordinates
instead of using `BoundaryHelperFunctions::FillRectilinearBoundaryData`.

I was unable to recreate this bug due to it regarding VisIt's parallel execution
context. On ix-dev, we only have access to VisIt's serial execution context.
The script I intended to use to recreate this bug is `bug5618.py`.

## Challenges

I ran into a number of challenges while trying to fix these bugs. In particular,
because the version of VisIt we have built on ix-dev is so limited, I was often
blocked by missing functionality, namely the lack of a SILO database reader and
support for parallel execution. I was able to set up a SILO database reader with
Hank's help. Another issue I often ran into was a lack of representative data.
A few issues did not provide the data they used to recreate the bug, and so I 
needed to scavenge for data or create my own. For \#20955 I was lucky enough to
get in contact with people who had access to the data, and they were able to
help me find it. Finally, it wasn't always clear if I had recreated a bug or if
I had created a bug of my own. Thus, I had to frequently double check my work.
The VisIt repository is also quite large and difficult to grasp in its entirety,
but using an LLM like Claude helped make working with the repository more
tractable.
