# Use rpmbuild --without gcj to disable native bits
%define with_gcj %{!?_without_gcj:1}%{?_without_gcj:0}

Name: sac
Version: 1.3
Release: 5.1%{?dist}
Summary: Java standard interface for CSS parser
License: W3C
Group: System Environment/Libraries
Source0: http://www.w3.org/2002/06/%{name}java-%{version}.zip
Source1: %{name}-build.xml
Source2: %{name}-MANIFEST.MF
URL: http://www.w3.org/Style/CSS/SAC/
BuildRequires: ant, java-devel, jpackage-utils
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: java, jpackage-utils
%if %{with_gcj}
BuildRequires: java-gcj-compat-devel >= 1.0.31
Requires(post): java-gcj-compat >= 1.0.31
Requires(postun): java-gcj-compat >= 1.0.31
%else
BuildArch: noarch
%endif

%description
SAC is a standard interface for CSS parsers, intended to work with CSS1, CSS2,
CSS3 and other CSS derived languages.

%package javadoc
Group: Development/Java
Summary: Javadoc for %{name}
%if %{with_gcj}
BuildArch: noarch
%endif

%description javadoc
Javadoc for %{name}.

%prep
%setup -q
install -m 644 %{SOURCE1} build.xml
find . -name "*.jar" -exec rm -f {} \;

%build
ant jar javadoc

%install
rm -rf $RPM_BUILD_ROOT

# inject OSGi manifests
mkdir -p META-INF
cp -p %{SOURCE2} META-INF/MANIFEST.MF
touch META-INF/MANIFEST.MF
zip -u build/lib/sac.jar META-INF/MANIFEST.MF

mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p ./build/lib/sac.jar $RPM_BUILD_ROOT%{_javadir}/sac.jar

mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -pr build/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}
%if %{with_gcj}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0644,root,root,0755)
%doc COPYRIGHT.html
%{_javadir}/%{name}.jar
%if %{with_gcj}
%attr(-,root,root) %{_libdir}/gcj/%{name}/%{name}.jar.*
%endif

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}

%changelog
* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 1.3-5.1
- Rebuilt for RHEL 6

* Fri Jul 24 2009 Caolan McNamara <caolanm@redhat.com> - 1.3-5
- make javadoc no-arch when building as arch-dependant aot

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-4.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 6 2009 Alexander Kurtakov <akurtako@redhat.com> 1.3-3.3
- Add osgi manifest (needed by eclipse-birt).

* Thu Jul 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.3-3.2
- drop repotag

* Fri May 09 2008 Caolan McNamara <caolanm@redhat.com> 1.3-3jpp.1
- update for guidelines

* Sat May 03 2008 Caolan McNamara <caolanm@redhat.com> 1.3-3jpp
- import from jpackage

* Fri Sep 03 2004 Fernando Nasser <fnasser@redhat.com> 1.3-3jpp
- Rebuild with Ant 1.6.2

* Tue May 06 2003 David Walluck <david@anti-microsoft.org> 1.3-2jpp
- update for JPackage 1.5

* Thu Jul 11 2002 Ville Skytte <ville.skytta at iki.fi> 1.3-1jpp
- Update to 1.3.
- Use sed instead of bash 2 extension when symlinking jars during build.
- Add Distribution tag, fix URL, tweak Summary and description.

* Wed Feb 06 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.2-1jpp 
- first jpp release
