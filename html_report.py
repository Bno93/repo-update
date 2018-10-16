import os
import time
from yattag import Doc

class HtmlReport(object):
  
  def __init__(self, report):

    self.__doc, self.__tag, self.__text = Doc().tagtext()
    self.__create_html_page(report)


  # end

  def __create_html_page(self, report):
    self.__doc.asis('<!DOCTYPE html>')
    with self.__tag('html'):
      self.__create_html_header()
      self.__create_html_body(report)
  # end

  def __create_html_header(self):
    with self.__tag('head'):
      with self.__tag('meta', charset='utf-8'):
          pass
      # end
      with self.__tag('meta', ("http-equiv", "X-UA-Compatible"), content="IE=edge"):
          pass
      # end
      with self.__tag('meta', name="viewport", content="width=device-width, initial-scale=1"):
          pass
      # end
      with self.__tag('title'):
          self.__text('Repo Report')
      # end
      with self.__tag('link', rel='stylesheet',
                href='https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css',
                integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u",
                crossorigin="anonymous"):
          pass
      # end
      with self.__tag('script', src='https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js'):
          pass
      # end
      with self.__tag('script', src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js",
                integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa",
                crossorigin="anonymous"):
          pass
      # end
      with self.__tag('script'):
        self.__text('$(document).ready(function () {\n')
        self.__text(
            "$('.repo').on('shown.bs.collapse', function() {$('.glyphicon').removeClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up');});\n")
        self.__text(
            "$('.repo').on('hidden.bs.collapse', function() {$('.glyphicon').removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down');});\n")
        self.__text('});')
      with self.__tag('style'):
          self.__text("#content{margin-left:10%;margin-right:10%;margin-top:1%;padding-left:10%;padding-right:10%;padding-top:1%;}\n")
          self.__text('span { float: right; }\n')
          self.__text('#heading{ margin:2%; }\n')
      # end
  # end

  def __choose_panel_status(self, status):
    if status == 'upToDate':
      return 'panel-success'
    elif status == 'updating':
      return 'panel-info'
    elif status == 'error' or status == 'conflict':
      return 'panel-danger'
    elif status == 'warning':
      return 'panel-warning'
    elif status == 'disabled':
      return 'panel-default'

  # end

  
  # private\mobilecomputing\mobilecomputing_programmentwurf
  def __create_id(self, name):
    html_id = str(name)
    html_id = html_id.replace(".", "")
    html_id = html_id.replace("\\", "-")
    html_id = html_id.replace(" ", "_")
    return html_id
  # end

  def __create_repo_panel_head(self, label, path):
    with self.__tag('div', klass='panel-heading'):
      self.__text(label)
      with self.__tag('span', ("data-toggle", "collapse"), ("data-target", "#{}".format(self.__create_id(path))),  klass="glyphicon glyphicon-chevron-down"):
        self.__text('')
      # end
    # end
  # end

  def __create_repo_panel_body(self, path, message):
    with self.__tag('div', klass='panel-body repo collapse', id='{}'.format(self.__create_id(path))):
     
      if type(message) is list:
        with self.__tag('ul', klass='list-group'):
          for line in message:
            with self.__tag('li', klass='list-group-item'):
              self.__text(str(line))
            # end
          # end
        # end
      # end
    # end
  # end

  def __create_repo_panel(self, repo):
    panelStatus = self.__choose_panel_status(repo['status'])

    with self.__tag('div', klass='panel ' + panelStatus):
      self.__create_repo_panel_head(repo['label'], repo['path'])
      self.__create_repo_panel_body(repo['path'], repo['message'])
    # end
  # end

  def __create_html_body(self, report):
    with self.__tag('body'):
      with self.__tag('div', klass='panel panel-default', id='heading'):
        with self.__tag('div', klass='panel-heading'):
            self.__text('Repo Update Report from ' + time.strftime('%H:%M %d.%m.%Y'))
            with self.__tag('span', ("data-toggle", "collapse"), ("data-target", "{}".format(".repo")), klass="glyphicon glyphicon-chevron-down"):
              self.__text('')
            # end
        # end  
        with self.__tag('div', klass='panel-body', id='content'):
          for repo in report['repos']:
            self.__create_repo_panel(repo)
          # end
        # end
      # end
    # end
  # end

  def get_html_report(self):
    return self.__doc.getvalue()
  # end

# end
