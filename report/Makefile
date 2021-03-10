STUDENT = С.Д. Бабошин
DEGREE = к.ф.-м.н.
DIRECTOR = М.Г. Завгородний

SED = "s/{{student}}/${STUDENT}/; s/{{degree}}/${DEGREE}/; s/{{director}}/${DIRECTOR}/"

all:
	# титульный лист
	sed -e ${SED} titlepage.fodt > tp-output.fodt
	libreoffice --headless --convert-to pdf tp-output.fodt

	# .tex
	pdflatex report.tex
	biber report
	pdflatex report.tex

	evince report.pdf &

clean:
	rm *.aux *.log *.out *.toc *.bbl *.bcf *.blg *.xml
	rm tp-output.*
