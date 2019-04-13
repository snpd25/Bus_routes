from flask import Flask, request, render_template
from flask import jsonify
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.jinja2')

@app.route('/route_finding', methods=['GET', 'POST'])
def route_finding():
	result = []
	result.append("OK")
	if request.method == 'POST':
		stop_f = request.form['stop_f']
		stop_t = request.form['stop_t']
		try:
			f = open('stop.txt', 'r')
			lines = f.readlines()
			f.close()
			flag=0

			for i, line in enumerate(lines):
				line = list(line.split(','))
				if stop_f == line[0] and i < len(lines):
					result.append(lines[i])
					flag+=1
				if stop_t == line[0] and i < len(lines):
					result.append(lines[i])
					flag+=1
				if flag==2:
					break
			if flag<2:
				result.append("Stop ID not found")

			if flag==2:
				g= open('stop_timing.txt','r')
				lines = g.readlines()
				g.close()
				flag_1=0
				time_1=[]
				time_2=[]
				trip=[]

				for i, line in enumerate(lines):
					line = list(line.split(','))
					if stop_f == line[3] and i < len(lines):
						#result.append(lines[i])
						time_1.append(line[0])
					if stop_t == line[3] and i < len(lines):
						#result.append(lines[i])
						time_2.append(line[0])

				for x in time_1:
					for y in time_2:
						if x==y:
							trip.append(x)
				if len(trip)==0:
					result.append("No direct root")
				else:
					#result.append(trip)
					flag_1=1

			if flag_1>0:
				h= open('trip.txt','r')
				lines = h.readlines()
				h.close()
				route=[]

				for i, line in enumerate(lines):
					line = list(line.split(','))
					line2= list(line[2].split('\n'))
					#result.append("debug")
					#result.append(line2[0])
					for o in trip:
						if (o == line2[0]) and i < len(lines):
							#result.append(lines[i])
							route.append(line[0])

				#result.append(route)

				p= open('route.txt','r')
				lines = p.readlines()
				p.close()

				result.append("Direct routes:")

				for i, line in enumerate(lines):
					line = list(line.split(','))
					line2= list(line[3].split('\n'))
					for x in route:
						if x == line2[0] and i < len(lines):
							result.append(lines[i])


					

		except EXCEPTION:
			pass
		return render_template('route_finding.jinja2', result= json.dumps(result))
	else:
		return render_template('route_finding.jinja2', result= json.dumps(result))


if __name__ == '__main__':
    app.debug = True
    app.run()