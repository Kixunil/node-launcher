from flask import request, render_template
from flask_admin import BaseView, expose

from node_launcher.node_set import NodeSet
from website.forms.request_capacity_form import RequestCapacityForm


class RequestCapacityView(BaseView):

    @expose('/')
    def index(self):
        form = RequestCapacityForm()
        node_set = NodeSet()
        address = node_set.lnd_client.get_new_address()
        return render_template('request_capacity.html',
                               form=form,
                               address=address)

    @expose('/buy_capacity', methods=['GET', 'POST'])
    def buy_channel(self):
        if request.method == 'POST':
            value = int(request.form['value'])
            memo = request.form['memo']
        else:
            value = 50000
            memo = 'Tip'
        node_set = NodeSet()
        payment_request = node_set.lnd_client.create_invoice(
            value=value,
            memo=memo
        ).payment_request
        uri = ':'.join(['lightning', payment_request])

        return render_template('payment_request.html',
                               payment_request=payment_request,
                               uri=uri)