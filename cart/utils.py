import logging
from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger(__name__)


def send_order_emails(order, product_summary, metodo_pago):
    try:
        # Mensaje para el cliente
        subject = 'Confirmación de Compra'
        customer_message = f"""
            Gracias por tu compra.
            Resumen de tu pedido:
                {product_summary}
            Total: Q{order.total_amount}
            Método de pago seleccionado: {metodo_pago}
            Pronto estaremos en contacto contigo para confirmar los detalles de tu pedido.
        """
        send_mail(subject, customer_message,
                  settings.DEFAULT_FROM_EMAIL, [order.user.email])
        logger.info(
            f"Correo de confirmación enviado al cliente {order.user.email} para la orden {order.id}")

        # Mensaje para el owner
        owner_message = f"""
            Nueva compra realizada por {order.user.email}
            Resumen del pedido:
                {product_summary}
            Total: Q{order.total_amount}
            Método de pago seleccionado: {metodo_pago}
        """
        send_mail(subject, owner_message,
                  settings.DEFAULT_FROM_EMAIL, [settings.OWNER_EMAIL])
        logger.info(
            f"Correo de notificación enviado al owner para la orden {order.id}")

    except Exception as e:
        logger.error(
            f"Error al enviar correos para la orden {order.id}: {str(e)}")
        raise  # Re-lanzar la excepción para manejarla en la vista
