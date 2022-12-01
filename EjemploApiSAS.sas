%global status;
%macro mensaje(txt=);

	data response;
		array MESSAGE_{7} $300 _TEMPORARY_ (&txt.);
		drop n;

		do n = 1 to 1;
			detail = MESSAGE_{n};
			output;
		end;
	run;

%mend;


%macro sendWeb(Tabla=);
	proc json out = _webout  pretty nosastags;
		write open object;
		write values "status" "&status";
		write values "datos";
		write open array;
		export &Tabla;
		write close;
		write close;
	run;
%mend;
%let status=OK;
%mensaje(txt="Mensaje de prueba para peticiones rest");
%sendWeb(Tabla=response);