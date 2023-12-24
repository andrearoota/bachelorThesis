\ProvidesClass{unibg}

\makeatletter

\newcommand{\@lang}{}
\newcommand{\@degtype}{}

\DeclareOption{italian}{\renewcommand{\@lang}{italian}}
\DeclareOption{english}{\renewcommand{\@lang}{english}}

\DeclareOption{master}{\renewcommand{\@degtype}{master}}
\DeclareOption{bachelor}{\renewcommand{\@degtype}{bachelor}}

\ExecuteOptions{italian,master}

\ProcessOptions\relax

\LoadClass[a4paper,12pt,twoside,openright]{report}

\RequirePackage[utf8]{inputenc}
\RequirePackage[backend=biber, sorting=none]{biblatex}
\RequirePackage[hidelinks]{hyperref}
\RequirePackage[T1]{fontenc}
\RequirePackage[\@lang]{babel}
\RequirePackage{amsmath}
\RequirePackage{caption}
\RequirePackage{subcaption}
\RequirePackage{csquotes}
\RequirePackage{fancyhdr}
\RequirePackage{geometry}
\RequirePackage{graphicx}
\RequirePackage{import}
\RequirePackage{listings}
\RequirePackage{float}
\RequirePackage{multicol}
\RequirePackage{xifthen}
\RequirePackage{xstring}
\RequirePackage{tabularx}

\DeclareStringOption[italian]{lang}

% ----------------------- Floating listings
\newfloat{lstfloat}{htbp}{lop}
\floatname{lstfloat}{Listing}
\def\lstfloatautorefname{Listing}


% ----------------------- Bibliography
\addbibresource{bibliography.bib}

% ----------------------- Graphics
\graphicspath{{./images/}}

% ----------------------- Page style
\fancypagestyle{plain}{
  \fancyhf{}
  \renewcommand{\headrulewidth}{0pt}
  \fancyfoot[CE,CO]{}
  \fancyfoot[LE,RO]{\thepage}
}
\pagestyle{plain}

% ----------------------- Geometry and measures
\geometry{margin=3cm}
\renewcommand{\baselinestretch}{1.5}
\setcounter{tocdepth}{4}

% ----------------------- New commands
\newcommand{\emptypage}{
  \clearpage
  \thispagestyle{empty}
  \pagenumbering{gobble}
  \mbox{}
}
\newcommand{\toc}[1][]{
  \clearpage
  \pagenumbering{Roman}
  \tableofcontents
  \IfSubStr{#1}{figures}{\listoffigures}{}
  \IfSubStr{#1}{tables}{\listoftables}{}
    \ifthenelse{\equal{\@lang}{italian}}
      {\renewcommand{\lstlistlistingname}{Elenco dei Codici}}
      {\renewcommand{\lstlistlistingname}{List of Listings}}
  \IfSubStr{#1}{listings}{\lstlistoflistings}{}
}

% ----------------------- Title page
\newcommand{\@subtitle}{}
\newcommand{\@coadvisor}{}

\newcommand{\subtitle}[1]{\renewcommand{\@subtitle}{#1}}
\newcommand{\department}[1]{\newcommand{\@department}{#1}}
\newcommand{\course}[1]{\newcommand{\@course}{#1}}
\newcommand{\class}[1]{\newcommand{\@class}{#1}}
\newcommand{\advisor}[1]{\newcommand{\@advisor}{#1}}
\newcommand{\coadvisor}[1]{\renewcommand{\@coadvisor}{#1}}
\newcommand{\studentid}[1]{\newcommand{\@studentid}{#1}}
\newcommand{\academicyear}[1]{\newcommand{\@academicyear}{#1}}

\newenvironment{changemargin}[2]{
  \list{}{\rightmargin#2\leftmargin#1}\item[]
}{
  \endlist
}

\renewcommand{\maketitle}{
  \newcommand{\@trDepartment}{\ifthenelse{\equal{\@lang}{italian}}{Dipartimento di}{Department of}}
  \newcommand{\@trCourseB}{\ifthenelse{\equal{\@lang}{italian}}{Corso di Laurea in}{Bachelor Degree in}}
  \newcommand{\@trCourseM}{\ifthenelse{\equal{\@lang}{italian}}{Corso di Laurea Triennale in}{Master Degree in}}
  \newcommand{\@trClass}{\ifthenelse{\equal{\@lang}{italian}}{Classe}{Class}}
  \newcommand{\@trAdvisor}{\ifthenelse{\equal{\@lang}{italian}}{Relatore}{Advisor}}
  \newcommand{\@trCoAdvisor}{\ifthenelse{\equal{\@lang}{italian}}{Correlatore}{Co-advisor}}
  \newcommand{\@trTesiLaureaB}{\ifthenelse{\equal{\@lang}{italian}}{Tesi di Laurea}{Thesis}}
  \newcommand{\@trTesiLaureaM}{\ifthenelse{\equal{\@lang}{italian}}{Tesi di Laurea Triennale}{Master Thesis}}
  \newcommand{\@trStudentNumber}{\ifthenelse{\equal{\@lang}{italian}}{Matricola n.}{Student number}}
  \newcommand{\@trAnnoAccademico}{\ifthenelse{\equal{\@lang}{italian}}{ANNO ACCADEMICO}{ACADEMIC YEAR}}

  \begin{titlepage}
    \ifthenelse{\equal{\@degtype}{master}}
      {
        \begin{center}
          \large
          UNIVERSITÀ DEGLI STUDI DI BERGAMO \\
          \vspace{0.5cm}
          \normalsize
          \@trDepartment~\@department \\
          \@trCourseM~\@course \\
          \@trClass~\@class
    
          \vfill
    
          \Huge
          \textbf{\@title}
    
          \LARGE
          \@subtitle
        \end{center}
    
        \vfill
    
        \begin{flushleft}
          \@trAdvisor \\
          \@advisor
        \end{flushleft}
    
        \ifthenelse{\equal{\@coadvisor}{}}{}{
          \begin{flushleft}
            \@trCoAdvisor \\
            \@coadvisor
          \end{flushleft}
        }
    
        \begin{flushright}
          {\@trTesiLaureaM} \\
          \@author \\
          \@trStudentNumber~\@studentid
        \end{flushright}
    
        \vfill
    
        \begin{center}
          \@trAnnoAccademico~\@academicyear
        \end{center}
      }
      {
        \newcommand{\@trCandidato}{\ifthenelse{\equal{\@lang}{italian}}{Candidato}{Candidate}}

        \includegraphics[width=8.79cm]{images/unibg-logo-wide.png}

        \vspace{0.5cm}

        \begin{changemargin}{4cm}{0cm}
          \@trDepartment \\
          \@department

          \vspace{0.5cm}

          \@trCourseB \\
          \@course

          \vspace{0.1cm}

          \@trClass~\@class

          \vfill

          {\Huge\textbf{\@title}}
    
          {\LARGE\@subtitle}

          \vfill

          \begin{multicols}{2}
          \@trCandidato: \\ \textit{\@author} \\
          \@trStudentNumber~\@studentid

          \columnbreak
          
          \@trAdvisor: \\ \textit{\@advisor}
          
          \vspace{0.5cm}
          
          \ifthenelse{\equal{\@coadvisor}{}}{}{\@trCoAdvisor: \\ \textit{\@coadvisor}}
          \end{multicols}

          \vfill

          \@trAnnoAccademico \\
          \@academicyear

        \end{changemargin}
      }
  \end{titlepage}
}

% ----------------------- JSON language
\usepackage{xcolor}

\colorlet{punct}{red!60!black}
\definecolor{delim}{RGB}{20,105,176}
\colorlet{numb}{magenta!60!black}

\lstdefinelanguage{json}{
    basicstyle=\normalfont\ttfamily,
    numbers=left,
    numberstyle=\scriptsize,
    stepnumber=1,
    numbersep=8pt,
    showstringspaces=false,
    breaklines=true,
    frame=lines,
    literate=
     *{0}{{{\color{numb}0}}}{1}
      {1}{{{\color{numb}1}}}{1}
      {2}{{{\color{numb}2}}}{1}
      {3}{{{\color{numb}3}}}{1}
      {4}{{{\color{numb}4}}}{1}
      {5}{{{\color{numb}5}}}{1}
      {6}{{{\color{numb}6}}}{1}
      {7}{{{\color{numb}7}}}{1}
      {8}{{{\color{numb}8}}}{1}
      {9}{{{\color{numb}9}}}{1}
      {:}{{{\color{punct}{:}}}}{1}
      {,}{{{\color{punct}{,}}}}{1}
      {\{}{{{\color{delim}{\{}}}}{1}
      {\}}{{{\color{delim}{\}}}}}{1}
      {[}{{{\color{delim}{[}}}}{1}
      {]}{{{\color{delim}{]}}}}{1},
}

% ----------------------- Javascript language

\lstdefinelanguage{JavaScript}{
  morekeywords=[1]{break, continue, delete, else, for, function, if, in,
    new, return, this, typeof, var, void, while, with},
  % Literals, primitive types, and reference types.
  morekeywords=[2]{false, null, true, boolean, number, undefined,
    Array, Boolean, Date, Math, Number, String, Object},
  % Built-ins.
  morekeywords=[3]{eval, parseInt, parseFloat, escape, unescape},
  sensitive,
  morecomment=[s]{/*}{*/},
  morecomment=[l]//,
  morecomment=[s]{/**}{*/}, % JavaDoc style comments
  morestring=[b]',
  morestring=[b]",
  numbers=left
}[keywords, comments, strings]

\makeatother

\endinput