%%
%% This is file `ecmwfrep.cls',
%% generated with the docstrip utility.
%%
%% The original source files were:
%%
%% classes.dtx  (with options: `tmemo')
%% 
%% This is a generated file.
%% 
%% Copyright 1993 1994 1995 1996 1997 1998 1999
%% The LaTeX3 Project and any individual authors listed elsewhere
%% in this file.
%% 
%% This file was generated from file(s) of the LaTeX base system.
%% --------------------------------------------------------------
%% 
%% It may be distributed and/or modified under the
%% conditions of the LaTeX Project Public License, either version 1.2
%% of this license or (at your option) any later version.
%% The latest version of this license is in
%%    http://www.latex-project.org/lppl.txt
%% and version 1.2 or later is part of all distributions of LaTeX
%% version 1999/12/01 or later.
%% 
%% This file may only be distributed together with a copy of the LaTeX
%% base system. You may however distribute the LaTeX base system without
%% such generated files.
%% 
%% The list of all files belonging to the LaTeX base distribution is
%% given in the file `manifest.txt'. See also `legal.txt' for additional
%% information.
%% 
%% \CharacterTable
%%  {Upper-case    \A\B\C\D\E\F\G\H\I\J\K\L\M\N\O\P\Q\R\S\T\U\V\W\X\Y\Z
%%   Lower-case    \a\b\c\d\e\f\g\h\i\j\k\l\m\n\o\p\q\r\s\t\u\v\w\x\y\z
%%   Digits        \0\1\2\3\4\5\6\7\8\9
%%   Exclamation   \!     Double quote  \"     Hash (number) \#
%%   Dollar        \$     Percent       \%     Ampersand     \&
%%   Acute accent  \'     Left paren    \(     Right paren   \)
%%   Asterisk      \*     Plus          \+     Comma         \,
%%   Minus         \-     Point         \.     Solidus       \/
%%   Colon         \:     Semicolon     \;     Less than     \<
%%   Equals        \=     Greater than  \>     Question mark \?
%%   Commercial at \@     Left bracket  \[     Backslash     \\
%%   Right bracket \]     Circumflex    \^     Underscore    \_
%%   Grave accent  \`     Left brace    \{     Vertical bar  \|
%%   Right brace   \}     Tilde         \~}
\NeedsTeXFormat{LaTeX2e}[1995/12/01]
\ProvidesClass{ecmwfrep}
              [2021/03/24 v0.91
 ECMWF LaTeX document class]
\newcommand\@ptsize{}
\newif\if@restonecol
\newif\if@titlepage
\newif\if@esarep
\RequirePackage{ifpdf}
%CM Set some variables
\newcommand{\series}[1]{\def\seriesname{#1}}   \series{Research Reports} %CM 
\newcommand{\seriesvolume}[1]{\def\seriesvolumename{#1}}  \seriesvolume{Research Report} %CM 
\newcommand{\seriesnumber}[1]{\def\memonumber{#1}}   \seriesnumber{?} %CM 
\newcommand{\subtitle}[1]{\def\subtitletext{#1}}   \subtitle{} %CM 
\newcommand{\ecmwfdepartment}[1]{\def\department{#1}}
                                    \ecmwfdepartment{Research Department} %CM 
\newcommand{\submitcomment}[1]{\def\subcomment{#1}} \submitcomment{}%CM 
\newcommand{\affiliation}[1]{\def\affiltext{#1}}    \affiliation{} %CM 
\newcommand{\headertitle}[1]{\def\httext{#1}}       \headertitle{\@title} %CM 
\newcommand{\coverauthor}[1]{\def\authorc{#1}}      \coverauthor{\@author} %CM 

\ifpdf                                                    
\RequirePackage[pdftex]{graphicx}                             
\pdfcompresslevel=9                                       
\else                                                     
\RequirePackage[dvips]{graphicx}                                     
\fi                                                       
\RequirePackage{mathptmx}           % to use PostScript fonts
\RequirePackage[scaled=0.92]{helvet}% to use PostScript fonts
\RequirePackage{courier}            % to use PostScript fonts
\RequirePackage{xcolor}             % to enable coloured text

%CM\DeclareOption{mytechmemo}{\department{rd}\ecdepartment{RESEARCH DEPARTMENT}\toname{DR}\series{Technical Memorandum}}
%cm \DeclareOption{mytechmemo}{\department{rd}}
\DeclareOption{techmemo}
   {\series{ECMWF Technical Memoranda}%
    \seriesvolume{Technical Memorandum}% 
    \newcommand{\@coverfile}{techmemo_cover}% 
    }
\DeclareOption{erareport}
   {\series{ERA Report Series}%
    \seriesvolume{ERA Report series No. }% 
    \newcommand{\@coverfile}{erareport_cover}% 
    }
\DeclareOption{eumetsat-ecmwf}
   {\series{EUMETSAT/ECMWF Fellowship Programme Research Reports}%
    \seriesvolume{EUMETSAT/ECMWF Fellowship Programme Research Report}% 
    \newcommand{\@coverfile}{eumetsat-ecmwf_cover}% 
    }
\DeclareOption{esareport}
   {\series{ECMWF ESA Contract Report Series}%
    \seriesvolume{ESA Contract Report}% 
    \newcommand{\@coverfile}{esareport_cover}% 
    \@esareptrue % 
    }

\@titlepagefalse
\if@compatibility\else

\DeclareOption{a4paper}
   {\setlength\paperheight {297mm}%
    \setlength\paperwidth  {210mm}}
\DeclareOption{a5paper}
   {\setlength\paperheight {210mm}%
    \setlength\paperwidth  {148mm}}
\DeclareOption{b5paper}
   {\setlength\paperheight {250mm}%
    \setlength\paperwidth  {176mm}}
\DeclareOption{letterpaper}
   {\setlength\paperheight {11in}%
    \setlength\paperwidth  {8.5in}}
\DeclareOption{legalpaper}
   {\setlength\paperheight {14in}%
    \setlength\paperwidth  {8.5in}}
\DeclareOption{executivepaper}
   {\setlength\paperheight {10.5in}%
    \setlength\paperwidth  {7.25in}}
\DeclareOption{landscape}
   {\setlength\@tempdima   {\paperheight}%
    \setlength\paperheight {\paperwidth}%
    \setlength\paperwidth  {\@tempdima}}
\fi
\if@compatibility
  \renewcommand\@ptsize{0}
\else
\DeclareOption{10pt}{\renewcommand\@ptsize{0}}
\fi
\DeclareOption{11pt}{\renewcommand\@ptsize{1}}
\DeclareOption{12pt}{\renewcommand\@ptsize{2}}
\if@compatibility\else
\DeclareOption{oneside}{\@twosidefalse \@mparswitchfalse}
\fi
\DeclareOption{twoside}{\@twosidetrue  \@mparswitchtrue}
\DeclareOption{draft}{\setlength\overfullrule{5pt}}
\if@compatibility\else
\DeclareOption{final}{\setlength\overfullrule{0pt}}
\fi
\DeclareOption{titlepage}{\@titlepagetrue}
\if@compatibility\else
\DeclareOption{notitlepage}{\@titlepagefalse}
\fi
\if@compatibility\else
\DeclareOption{onecolumn}{\@twocolumnfalse}
\fi
\DeclareOption{twocolumn}{\@twocolumntrue}
\DeclareOption{leqno}{\input{leqno.clo}}
\DeclareOption{fleqn}{\input{fleqn.clo}}
\DeclareOption{openbib}{%
  \AtEndOfPackage{%
   \renewcommand\@openbib@code{%
      \advance\leftmargin\bibindent
      \itemindent -\bibindent
      \listparindent \itemindent
      \parsep \z@
      }%
   \renewcommand\newblock{\par}}%
}
%CM\ExecuteOptions{letterpaper,10pt,oneside,onecolumn,final}
\ExecuteOptions{a4paper,11pt,twoside,onecolumn,final}
\ProcessOptions
\input{size1\@ptsize.clo}
\setlength\lineskip{1\p@}
\setlength\normallineskip{1\p@}
\renewcommand\baselinestretch{}
\setlength\parskip{0\p@ \@plus \p@}
\@lowpenalty   51
\@medpenalty  151
\@highpenalty 301
\setcounter{topnumber}{2}
\renewcommand\topfraction{.7}
\setcounter{bottomnumber}{1}
\renewcommand\bottomfraction{.3}
\setcounter{totalnumber}{3}
\renewcommand\textfraction{.2}
\renewcommand\floatpagefraction{.5}
\setcounter{dbltopnumber}{2}
\renewcommand\dbltopfraction{.7}
\renewcommand\dblfloatpagefraction{.5}
\if@twoside
  \def\ps@headings{%
      \let\@oddfoot\@empty\let\@evenfoot\@empty
      \def\@evenhead{\thepage\hfil\slshape\leftmark}%
      \def\@oddhead{{\slshape\rightmark}\hfil\thepage}%
      \let\@mkboth\markboth
    \def\sectionmark##1{%
      \markboth {\MakeUppercase{%
        \ifnum \c@secnumdepth >\z@
          \thesection\quad
        \fi
        ##1}}{}}%
    \def\subsectionmark##1{%
      \markright {%
        \ifnum \c@secnumdepth >\@ne
          \thesubsection\quad
        \fi
        ##1}}}
\else
  \def\ps@headings{%
    \let\@oddfoot\@empty
    \def\@oddhead{{\slshape\rightmark}\hfil\thepage}%
    \let\@mkboth\markboth
    \def\sectionmark##1{%
      \markright {\MakeUppercase{%
        \ifnum \c@secnumdepth >\m@ne
          \thesection\quad
        \fi
        ##1}}}}
\fi
\def\ps@myheadings{%
    \let\@oddfoot\@empty\let\@evenfoot\@empty
    \def\@evenhead{\thepage\hfil\slshape\leftmark}%
    \def\@oddhead{{\slshape\rightmark}\hfil\thepage}%
    \let\@mkboth\@gobbletwo
    \let\sectionmark\@gobble
    \let\subsectionmark\@gobble
    }
  \if@titlepage
  \newcommand\maketitle{\begin{titlepage}%
  \let\footnotesize\small
  \let\footnoterule\relax
  \let \footnote \thanks
  \null\vfil
  \vskip 60\p@
  \begin{center}%
    {\LARGE \@title \par}%
    \vskip 3em%
    {\large
     \lineskip .75em%
      \begin{tabular}[t]{c}%
        \@author
      \end{tabular}\par}%
      \vskip 1.5em%
    {\large \@date \par}%       % Set date in \large size.
  \end{center}\par
  \@thanks
  \vfil\null
  \end{titlepage}%
  \setcounter{footnote}{0}%
  \global\let\thanks\relax
  \global\let\maketitle\relax
  \global\let\@thanks\@empty
  \global\let\@author\@empty
  \global\let\@date\@empty
%CM  \global\let\@title\@empty
%CM  \global\let\title\relax
  \global\let\author\relax
  \global\let\date\relax
  \global\let\and\relax
}
\else
\newcommand\maketitle{\par
  \begingroup
%CM    \renewcommand\thefootnote{\@fnsymbol\c@footnote}%
%CM    \renewcommand\thefootnote{\@fnsymbol\c@footnote}%
    \def\@makefnmark{\rlap{\@textsuperscript{\normalfont\@thefnmark}}}%
    \long\def\@makefntext##1{\parindent 1em\noindent
            \hb@xt@1.8em{%
                \hss\@textsuperscript{\normalfont\@thefnmark}}##1}%
    \if@twocolumn
      \ifnum \col@number=\@ne
        \@maketitle
      \else
        \twocolumn[\@maketitle]%
      \fi
    \else
      \newpage
      \global\@topnum\z@   % Prevents figures from going at top of page.
      \@maketitle
    \fi
%CM     \thispagestyle{plain}\@thanks
    \thispagestyle{fancy}\@thanks %CM does heading on first page
  \endgroup
  \setcounter{footnote}{0}%
  \global\let\thanks\relax
  \global\let\maketitle\relax
  \global\let\@maketitle\relax
  \global\let\@thanks\@empty
  \global\let\@author\@empty
  \global\let\@date\@empty
%CM  \global\let\@title\@empty
%CM  \global\let\title\relax
  \global\let\author\relax
  \global\let\date\relax
  \global\let\and\relax
}

\def\@maketitle{%
  \newpage        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% titlepage 
\thispagestyle{empty}
\setlength{\unitlength}{1mm}
\sffamily

\if@esarep          %%%%%%%%%%%%%%%%%%%%%%%% if ESA report

\ifpdf                            % PDF
\begin{picture}(250,230)(23,15)
\else                             % EPS/PostScript 
\begin{picture}(250,230)(25,10)
\fi
%CM \put(0,-15){\includegraphics{ee_cover}}
%cm\put(0,-15){\includegraphics{tm_cover}}
\put(0,-15){\includegraphics{\@coverfile}}

\put(14,208){\begin{minipage}[t][111mm]{105mm}\raggedright
\fontsize{15}{45}\selectfont \memonumber \par \vskip 50pt
\color{white}
\fontseries{b}\fontsize{25}{29}\selectfont \@title \par \vskip 5pt
\fontseries{m}\fontsize{12}{14}\selectfont \subtitletext \par 
\vfill
\fontseries{m}\fontsize{14}{17}\selectfont \authorc %CM\par 
\end{minipage} }
\put(14,95){\color{white}\fontseries{b}\fontsize{12}{15}\selectfont \@date} %CM  \par \vskip 1em
\end{picture}

\else          %%%%%%%%%%%%%%%%%%%%%%%% if other report

\ifpdf                            % PDF
\begin{picture}(250,230)(23,15)
\else                             % EPS/PostScript 
\begin{picture}(250,230)(25,10)
\fi
%CM \put(0,-15){\includegraphics{ee_cover}}
%cm\put(0,-15){\includegraphics{tm_cover}}
\put(0,-15){\includegraphics{\@coverfile}}

\put(14,208){\begin{minipage}[t][115mm]{105mm}\raggedright
\fontsize{44}{40}\selectfont \memonumber \par \vskip 25pt
\color{white}
\fontseries{b}\fontsize{20}{25}\selectfont \@title \par \vfill
\fontseries{m}\fontsize{8}{8}\selectfont \authorc %CM\par 
\end{minipage} }
\put(14,95){\color{white}\fontseries{b}\fontsize{12}{15}\selectfont \@date} %CM  \par \vskip 1em
\end{picture}

\fi

\newpage %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% titlepage reverse

\thispagestyle{empty}\sffamily \fontsize{9.5}{11}\selectfont
Series: \seriesname

A full list of ECMWF Publications can be found on our web site under:\\
\def\UrlFont{\em}
\url{http://www.ecmwf.int/en/publications/}

Contact: library@ecmwf.int

\vfill
\copyright\ Copyright \number\year

European Centre for Medium Range Weather Forecasts,
Shinfield Park,
Reading, RG2 9AX, UK

Literary and scientific copyrights belong to ECMWF and are reserved in all countries. The content of this 
document is available for use under a Creative Commons Attribution 4.0 International Public License.\\
See the terms at \url{https://creativecommons.org/licenses/by/4.0/}.

The information within this publication is given in good faith and considered to be true, but ECMWF 
accepts no liability for error or omission or for loss or damage arising from its use.

\newpage \thispagestyle{empty} \pagestyle{fancy} ~ 
% \newpage
\setcounter{page}{1}}
\fi

\setcounter{secnumdepth}{3}
\newcounter {part}
\newcounter {section}
\newcounter {subsection}[section]
\newcounter {subsubsection}[subsection]
\newcounter {paragraph}[subsubsection]
\newcounter {subparagraph}[paragraph]
\renewcommand \thepart {\@Roman\c@part}
\renewcommand \thesection {\@arabic\c@section}
\renewcommand\thesubsection   {\thesection.\@arabic\c@subsection}
\renewcommand\thesubsubsection{\thesubsection .\@arabic\c@subsubsection}
\renewcommand\theparagraph    {\thesubsubsection.\@arabic\c@paragraph}
\renewcommand\thesubparagraph {\theparagraph.\@arabic\c@subparagraph}
\newcommand\part{%
   \if@noskipsec \leavevmode \fi
   \par
   \addvspace{4ex}%
   \@afterindentfalse
   \secdef\@part\@spart}

\def\@part[#1]#2{%
    \ifnum \c@secnumdepth >\m@ne
      \refstepcounter{part}%
      \addcontentsline{toc}{part}{\thepart\hspace{1em}#1}%
    \else
      \addcontentsline{toc}{part}{#1}%
    \fi
    {\parindent \z@ \raggedright
     \interlinepenalty \@M
     \normalfont
     \ifnum \c@secnumdepth >\m@ne
       \Large\bfseries \partname~\thepart
       \par\nobreak
     \fi
     \huge \bfseries #2%
     \markboth{}{}\par}%
    \nobreak
    \vskip 3ex
    \@afterheading}
\def\@spart#1{%
    {\parindent \z@ \raggedright
     \interlinepenalty \@M
     \normalfont
     \huge \bfseries #1\par}%
     \nobreak
     \vskip 3ex
     \@afterheading}
\newcommand\section{\@startsection {section}{1}{\z@}%
                                   {-3.5ex \@plus -1ex \@minus -.2ex}%
                                   {2.3ex \@plus.2ex}%
                                   {\normalfont\Large\bfseries}}
\newcommand\subsection{\@startsection{subsection}{2}{\z@}%
                                     {-3.25ex\@plus -1ex \@minus -.2ex}%
                                     {1.5ex \@plus .2ex}%
                                     {\normalfont\large\bfseries}}
\newcommand\subsubsection{\@startsection{subsubsection}{3}{\z@}%
                                     {-3.25ex\@plus -1ex \@minus -.2ex}%
                                     {1.5ex \@plus .2ex}%
%CM                                     {\normalfont\normalsize\bfseries}}
                                     {\normalfont\normalsize\itshape}}
\newcommand\paragraph{\@startsection{paragraph}{4}{\z@}%
                                    {3.25ex \@plus1ex \@minus.2ex}%
                                    {-1em}%
                                    {\normalfont\normalsize\bfseries}}
\newcommand\subparagraph{\@startsection{subparagraph}{5}{\parindent}%
                                       {3.25ex \@plus1ex \@minus .2ex}%
                                       {-1em}%
                                      {\normalfont\normalsize\bfseries}}
\if@twocolumn
  \setlength\leftmargini  {2em}
\else
  \setlength\leftmargini  {2.5em}
\fi
\leftmargin  \leftmargini
\setlength\leftmarginii  {2.2em}
\setlength\leftmarginiii {1.87em}
\setlength\leftmarginiv  {1.7em}
\if@twocolumn
  \setlength\leftmarginv  {.5em}
  \setlength\leftmarginvi {.5em}
\else
  \setlength\leftmarginv  {1em}
  \setlength\leftmarginvi {1em}
\fi
\setlength  \labelsep  {.5em}
\setlength  \labelwidth{\leftmargini}
\addtolength\labelwidth{-\labelsep}
\@beginparpenalty -\@lowpenalty
\@endparpenalty   -\@lowpenalty
\@itempenalty     -\@lowpenalty
\renewcommand\theenumi{\@arabic\c@enumi}
\renewcommand\theenumii{\@alph\c@enumii}
\renewcommand\theenumiii{\@roman\c@enumiii}
\renewcommand\theenumiv{\@Alph\c@enumiv}
\newcommand\labelenumi{\theenumi.}
\newcommand\labelenumii{(\theenumii)}
\newcommand\labelenumiii{\theenumiii.}
\newcommand\labelenumiv{\theenumiv.}
\renewcommand\p@enumii{\theenumi}
\renewcommand\p@enumiii{\theenumi(\theenumii)}
\renewcommand\p@enumiv{\p@enumiii\theenumiii}
\newcommand\labelitemi{\textbullet}
\newcommand\labelitemii{\normalfont\bfseries \textendash}
\newcommand\labelitemiii{\textasteriskcentered}
\newcommand\labelitemiv{\textperiodcentered}
\newenvironment{description}
               {\list{}{\labelwidth\z@ \itemindent-\leftmargin
                        \let\makelabel\descriptionlabel}}
               {\endlist}
\newcommand*\descriptionlabel[1]{\hspace\labelsep
                                \normalfont\bfseries #1}
\if@titlepage
  \newenvironment{abstract}{%
      \titlepage
      \null\vfil
      \@beginparpenalty\@lowpenalty
%CM      \begin{center}%
        \bfseries \abstractname
        \@endparpenalty\@M
%CM       \end{center}}%
     {\par\vfil\null\endtitlepage}
\else
  \newenvironment{abstract}{%
      \pagestyle{fancy}%CM \pagestyle{empty}
      \if@twocolumn
        \section*{\abstractname}%
      \else
        \small
%CM        \begin{center}%
          {\bfseries \abstractname\vspace{-.5em}\vspace{\z@}}%
%CM        \end{center}%
%CM           \parindent 0pt
           \quotation 
      \fi}
      {\if@twocolumn\else\endquotation\fi}
\fi
\newenvironment{verse}
               {\let\\\@centercr
                \list{}{\itemsep      \z@
                        \itemindent   -1.5em%
                        \listparindent\itemindent
                        \rightmargin  \leftmargin
                        \advance\leftmargin 1.5em}%
                \item\relax}
               {\endlist}
\newenvironment{quotation}
%CM               {\list{}{\listparindent 1.5em%
               {\list{}{\listparindent 0em%
                        \itemindent    \listparindent
                        \rightmargin   \leftmargin
                        \parsep        \z@ \@plus\p@
                        \parsep 1.5ex %CM
                        }%
                \item\relax}
               {\endlist}
\newenvironment{quote}
               {\list{}{\rightmargin\leftmargin}%
                \item\relax}
               {\endlist}
\if@compatibility
\newenvironment{titlepage}
    {%
      \if@twocolumn
        \@restonecoltrue\onecolumn
      \else
        \@restonecolfalse\newpage
      \fi
%CM      \thispagestyle{empty}%
      \thispagestyle{fancy}%
      \setcounter{page}\z@
    }%
    {\if@restonecol\twocolumn \else \newpage \fi
    }
\else
\newenvironment{titlepage}
    {%
      \if@twocolumn
        \@restonecoltrue\onecolumn
      \else
        \@restonecolfalse\newpage
      \fi
%CM      \thispagestyle{empty}%
      \thispagestyle{fancy}%
      \setcounter{page}\@ne
    }%
    {\if@restonecol\twocolumn \else \newpage \fi
     \if@twoside\else
        \setcounter{page}\@ne
     \fi
    }
\fi
\newcommand\appendix{\par
  \setcounter{section}{0}%
  \setcounter{subsection}{0}%
  \gdef\thesection{\@Alph\c@section}}
\setlength\arraycolsep{5\p@}
\setlength\tabcolsep{6\p@}
\setlength\arrayrulewidth{.4\p@}
\setlength\doublerulesep{2\p@}
\setlength\tabbingsep{\labelsep}
\skip\@mpfootins = \skip\footins
\setlength\fboxsep{3\p@}
\setlength\fboxrule{.4\p@}
\renewcommand \theequation {\@arabic\c@equation}
\newcounter{figure}
\renewcommand \thefigure {\@arabic\c@figure}
\def\fps@figure{tbp}
\def\ftype@figure{1}
\def\ext@figure{lof}
\def\fnum@figure{\figurename~\thefigure}
\newenvironment{figure}
               {\@float{figure}}
               {\end@float}
\newenvironment{figure*}
               {\@dblfloat{figure}}
               {\end@dblfloat}
\newcounter{table}
\renewcommand\thetable{\@arabic\c@table}
\def\fps@table{tbp}
\def\ftype@table{2}
\def\ext@table{lot}
\def\fnum@table{\tablename~\thetable}
\newenvironment{table}
               {\@float{table}}
               {\end@float}
\newenvironment{table*}
               {\@dblfloat{table}}
               {\end@dblfloat}
\newlength\abovecaptionskip
\newlength\belowcaptionskip
\setlength\abovecaptionskip{10\p@}
\setlength\belowcaptionskip{0\p@}
\long\def\@makecaption#1#2{%
  \vskip\abovecaptionskip 
  \sbox\@tempboxa{\itshape\small{}#1: #2}% 
%ML  \sbox\@tempboxa{#1: #2}% 
  \ifdim \wd\@tempboxa >\hsize
%ML    #1: #2\par 
    \itshape\small{}#1: #2\par
  \else
    \global \@minipagefalse
    \hb@xt@\hsize{\hfil\box\@tempboxa\hfil}%
  \fi
  \vskip\belowcaptionskip}
\DeclareOldFontCommand{\rm}{\normalfont\rmfamily}{\mathrm}
\DeclareOldFontCommand{\sf}{\normalfont\sffamily}{\mathsf}
\DeclareOldFontCommand{\tt}{\normalfont\ttfamily}{\mathtt}
\DeclareOldFontCommand{\bf}{\normalfont\bfseries}{\mathbf}
\DeclareOldFontCommand{\it}{\normalfont\itshape}{\mathit}
\DeclareOldFontCommand{\sl}{\normalfont\slshape}{\@nomath\sl}
\DeclareOldFontCommand{\sc}{\normalfont\scshape}{\@nomath\sc}
\DeclareRobustCommand*\cal{\@fontswitch\relax\mathcal}
\DeclareRobustCommand*\mit{\@fontswitch\relax\mathnormal}
\newcommand\@pnumwidth{1.55em}
\newcommand\@tocrmarg{2.55em}
\newcommand\@dotsep{4.5}
\setcounter{tocdepth}{3}
\newcommand\tableofcontents{%
    \section*{\contentsname
        \@mkboth{%
           \MakeUppercase\contentsname}{\MakeUppercase\contentsname}}%
    \@starttoc{toc}%
    }
\newcommand*\l@part[2]{%
  \ifnum \c@tocdepth >-2\relax
    \addpenalty\@secpenalty
    \addvspace{2.25em \@plus\p@}%
    \begingroup
      \parindent \z@ \rightskip \@pnumwidth
      \parfillskip -\@pnumwidth
      {\leavevmode
       \large \bfseries #1\hfil \hb@xt@\@pnumwidth{\hss #2}}\par
       \nobreak
       \if@compatibility
         \global\@nobreaktrue
         \everypar{\global\@nobreakfalse\everypar{}}%
      \fi
    \endgroup
  \fi}
\newcommand*\l@section[2]{%
  \ifnum \c@tocdepth >\z@
    \addpenalty\@secpenalty
    \addvspace{1.0em \@plus\p@}%
    \setlength\@tempdima{1.5em}%
    \begingroup
      \parindent \z@ \rightskip \@pnumwidth
      \parfillskip -\@pnumwidth
      \leavevmode \bfseries
      \advance\leftskip\@tempdima
      \hskip -\leftskip
      #1\nobreak\hfil \nobreak\hb@xt@\@pnumwidth{\hss #2}\par
    \endgroup
  \fi}
\newcommand*\l@subsection{\@dottedtocline{2}{1.5em}{2.3em}}
\newcommand*\l@subsubsection{\@dottedtocline{3}{3.8em}{3.2em}}
\newcommand*\l@paragraph{\@dottedtocline{4}{7.0em}{4.1em}}
\newcommand*\l@subparagraph{\@dottedtocline{5}{10em}{5em}}
\newcommand\listoffigures{%
    \section*{\listfigurename
      \@mkboth{\MakeUppercase\listfigurename}%
              {\MakeUppercase\listfigurename}}%
    \@starttoc{lof}%
    }
\newcommand*\l@figure{\@dottedtocline{1}{1.5em}{2.3em}}
\newcommand\listoftables{%
    \section*{\listtablename
      \@mkboth{%
          \MakeUppercase\listtablename}{\MakeUppercase\listtablename}}%
    \@starttoc{lot}%
    }
\let\l@table\l@figure
\newdimen\bibindent
\setlength\bibindent{1.5em}
\newenvironment{thebibliography}[1]
     {\section*{\refname
        \@mkboth{\MakeUppercase\refname}{\MakeUppercase\refname}}%
      \list{\@biblabel{\@arabic\c@enumiv}}%
           {\settowidth\labelwidth{\@biblabel{#1}}%
            \leftmargin\labelwidth
            \advance\leftmargin\labelsep
            \@openbib@code
            \usecounter{enumiv}%
            \let\p@enumiv\@empty
            \renewcommand\theenumiv{\@arabic\c@enumiv}}%
      \sloppy
      \clubpenalty4000
      \@clubpenalty \clubpenalty
      \widowpenalty4000%
      \sfcode`\.\@m}
     {\def\@noitemerr
       {\@latex@warning{Empty `thebibliography' environment}}%
      \endlist}
\newcommand\newblock{\hskip .11em\@plus.33em\@minus.07em}
\let\@openbib@code\@empty
\newenvironment{theindex}
               {\if@twocolumn
                  \@restonecolfalse
                \else
                  \@restonecoltrue
                \fi
                \columnseprule \z@
                \columnsep 35\p@
                \twocolumn[\section*{\indexname}]%
                \@mkboth{\MakeUppercase\indexname}%
                        {\MakeUppercase\indexname}%
                \thispagestyle{plain}\parindent\z@
                \parskip\z@ \@plus .3\p@\relax
                \let\item\@idxitem}
               {\if@restonecol\onecolumn\else\clearpage\fi}
\newcommand\@idxitem{\par\hangindent 40\p@}
\newcommand\subitem{\@idxitem \hspace*{20\p@}}
\newcommand\subsubitem{\@idxitem \hspace*{30\p@}}
\newcommand\indexspace{\par \vskip 10\p@ \@plus5\p@ \@minus3\p@\relax}
\renewcommand\footnoterule{%
  \kern-3\p@
  \hrule\@width.4\columnwidth
  \kern2.6\p@}
\newcommand\@makefntext[1]{%
    \parindent 1em%
    \noindent
    \hb@xt@1.8em{\hss\@makefnmark}#1}
\newcommand\contentsname{Contents}
\newcommand\listfigurename{List of Figures}
\newcommand\listtablename{List of Tables}
\newcommand\refname{References}
\newcommand\indexname{Index}
\newcommand\figurename{Figure}
\newcommand\tablename{Table}
\newcommand\partname{Part}
\newcommand\appendixname{Appendix}
\newcommand\abstractname{Abstract}

\def\today{\ifcase\month\or
  January\or February\or March\or April\or May\or June\or
  July\or August\or September\or October\or November\or December\fi
  \space\number\day, \number\year}
\setlength\columnsep{10\p@}
\setlength\columnseprule{0\p@}
\pagenumbering{arabic}
\if@twoside
\else
  \raggedbottom
\fi
\if@twocolumn
  \twocolumn
  \sloppy
  \flushbottom
\else
  \onecolumn
\fi

%CMCMCMCCMCMCMCMCMCMCMCMCMCMCMCMCMCMCMCMCMCMCMCMCMCMCMCMCMCMCMMCMCM

\textwidth 160mm
\textheight 231mm
\setlength{\parskip}{1.5ex}
\setlength{\parindent}{0cm}
\topmargin -9mm
\headsep 5mm
\headheight 43pt %CM 20091008
\footskip 15mm
\oddsidemargin -1mm
\evensidemargin 3mm

% these settings should work fine with pdflatex/Acrobat 5.0
% 2cm margins are achieved when printed WITHOUT shrinking
% \setlength{\pdfvorigin}{18truemm}
% \setlength{\pdfhorigin}{22truemm}
\setlength{\pdfvorigin}{26truemm}
\setlength{\pdfhorigin}{24truemm}

\ifpdf 
  \DeclareGraphicsExtensions{.pdf,.jpg,.mps,.png} 
\else                                             
  \DeclareGraphicsExtensions{.eps,.eps.gz,.ps,.ps.gz,.jpg,.mps,.png} 
%   \DeclareGraphicsRule{.ps.gz}{eps}{.bb}{`gunzip -c #1}    
%   \DeclareGraphicsRule{.eps.gz}{eps}{.bb}{`gunzip -c #1}    
\fi                                                                                

\RequirePackage[bookmarks=true,bookmarksopen=true,bookmarksnumbered=true,colorlinks=true,
linkcolor=blue,
anchorcolor=blue,
urlcolor=blue,
citecolor=blue]{hyperref}  
%CM \RequirePackage[bookmarks=true,bookmarksopen=true,bookmarksnumbered=true]{hyperref}  
\RequirePackage{fancyhdr}
\pagestyle{fancy}%CM


%\newcommand{\littlelogo}{\raisebox{-1.4mm}{\includegraphics[width=7mm]{ecmwflogo_bw}}}
\newcommand{\littlelogo}{\raisebox{-0.9mm}{\includegraphics[width=22mm]{ECMWF_new_logo}}}


%%%% example of header/footer redefinition for an RD memo :

\renewcommand{\headrule}%
{\vspace*{-26pt} \rule{\textwidth}{1pt} %
\raisebox{-1ex}{\rule{\textwidth}{1pt}} %
 \vspace*{5.5ex}\hspace*{-\textwidth}   }

\renewcommand{\footrule}{\raisebox{2.5ex}{\rule{\textwidth}{1pt}\hspace*{-\textwidth}}} 

\fancyhead[LE,RO]{\littlelogo}
%\fancyhead[LO]{\small \sf \rightmark}
\fancyhead[LO]{\small \httext}
\fancyhead[RE]{\small \httext}
\if@esarep
\fancyfoot[LO,RE]{\small \seriesvolumename }
\else
\fancyfoot[LO,RE]{\small \seriesvolumename { }\memonumber}
\fi
\fancyfoot[LE,RO]{\small \thepage}
\fancyfoot[C]{}                                                                    

% Other macros
\def\proc#1{\medbreak\noindent{\it #1}\hspace{1ex}\ignorespaces}
\def\rd{\mbox{\rm d}}
\def\rD{\mbox{\rm D}}
\def\degree{\mbox{\hbox to .25em{}$^\circ$}}
\def\dg{\mbox{$^\circ$}}
\def\mdot{\mbox{\,\raise2pt\hbox{\bf .}}\,}
\def\degC{\degree{}C}
\def\and{{\textup{and}}}
\def\doublespacing{\renewcommand{\baselinestretch}{2}}

\endinput
%%
%% End of file `eumetsat-ecmwf.cls'.
