Name:           antlr4
Version:        4.5
Release:        3%{?dist}
Summary:        Java parser generator
License:        BSD
URL:            http://www.antlr.org/
BuildArch:      noarch

Source0:        https://github.com/antlr/antlr4/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz

# Upstream uses an experimental bulid tool (http://bildtool.org/),
# which is not available in Fedora.  RPMs are built with Maven using
# POMs maintained by package maintainer.
Source1:        antlr4-runtime.pom
Source2:        antlr4-tool.pom
Source3:        antlr4-maven-plugin.pom
Source4:        antlr4-aggregator.pom

BuildRequires:  maven-local
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.abego.treelayout:org.abego.treelayout.core)
BuildRequires:  mvn(org.antlr:antlr3-maven-plugin)
BuildRequires:  mvn(org.antlr:antlr4-maven-plugin)
BuildRequires:  mvn(org.antlr:antlr-runtime)
BuildRequires:  mvn(org.antlr:ST4)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.apache.maven:maven-core)
BuildRequires:  mvn(org.apache.maven:maven-plugin-api)
BuildRequires:  mvn(org.apache.maven.plugin-tools:maven-plugin-annotations)
BuildRequires:  mvn(org.apache.maven.shared:maven-plugin-testing-harness)
BuildRequires:  mvn(org.codehaus.plexus:plexus-compiler-api)
BuildRequires:  mvn(org.sonatype.plexus:plexus-build-api)


%description
ANTLR (ANother Tool for Language Recognition) is a powerful parser
generator for reading, processing, executing, or translating
structured text or binary files.  It's widely used to build languages,
tools, and frameworks. From a grammar, ANTLR generates a parser that
can build and walk parse trees.

%package runtime
Summary:        ANTLR runtime

%description runtime
This package provides runtime library used by parsers generated by
ANTLR.

%package maven-plugin
Summary:        ANTLR plugin for Apache Maven

%description maven-plugin
This package provides plugin for Apache Maven which can be used to
generate ANTLR parsers during build.

%package javadoc
Summary:        API documentation for %{name}

%description javadoc
This package contains %{summary}.

%prep
%setup -q
cp -a %{SOURCE1} runtime/Java/pom.xml
cp -a %{SOURCE2} tool/pom.xml
cp -a %{SOURCE3} antlr4-maven-plugin/pom.xml
cp -a %{SOURCE4} pom.xml
find -name \*.jar -delete

%mvn_package :aggregator-project __noinstall

%build
%mvn_build -s

%install
%mvn_install

%jpackage_script org.antlr.v4.Tool "" "" antlr4/antlr4:antlr3-runtime:antlr4/antlr4-runtime:stringtemplate4:treelayout %{name} true

%files -f .mfiles-antlr4
%{_bindir}/%{name}
%doc tool/MIGRATION.txt

%files runtime -f .mfiles-antlr4-runtime
%doc CHANGES.txt README.md
%license LICENSE.txt

%files maven-plugin -f .mfiles-antlr4-maven-plugin

%files javadoc -f .mfiles-javadoc
%license LICENSE.txt

%changelog
* Tue Mar 31 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.5-3
- Non-bootstrap build

* Mon Mar 30 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.5-2
- Post-review cleanup

* Thu Mar 26 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.5-1
- Initial packaging
