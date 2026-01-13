from flask import Blueprint, jsonify
from app.services.automation_service import AutomationService
from app.services.reporting_service import ReportingService
from app.services.performance_tracking_service import PerformanceTrackingService
from app.services.backup_service import BackupService
from app.utils.error_handler import handle_error

bp = Blueprint('automation', __name__)
automation_service = AutomationService()
reporting_service = ReportingService()
performance_service = PerformanceTrackingService()
backup_service = BackupService()

@bp.route('/morning-setup', methods=['POST'])
def morning_setup():
    """Run morning setup automation - SmartScout + Google Sheets + Duplicate Detection"""
    try:
        from flask import request
        data = request.get_json() or {}
        
        # Get parameters
        smartscout_enabled = data.get('smartscout_enabled', True)
        brand_count = data.get('brand_count', 100)
        
        results = automation_service.morning_setup(
            smartscout_enabled=smartscout_enabled,
            brand_count=brand_count
        )
        
        return jsonify({
            'success': True,
            'message': 'Morning setup completed (90% Automated)',
            'data': results
        }), 200
    except Exception as e:
        return handle_error(e)

@bp.route('/end-of-day', methods=['POST'])
def end_of_day():
    """Run end of day automation"""
    try:
        results = automation_service.end_of_day_tasks()
        return jsonify({
            'success': True,
            'message': 'End of day tasks completed',
            'data': results
        }), 200
    except Exception as e:
        return handle_error(e)

@bp.route('/daily-report', methods=['GET'])
def get_daily_report():
    """Get daily report"""
    try:
        report = reporting_service.generate_daily_report()
        return jsonify({
            'success': True,
            'data': report
        }), 200
    except Exception as e:
        return handle_error(e)

@bp.route('/weekly-summary', methods=['GET'])
def get_weekly_summary():
    """Get weekly summary"""
    try:
        summary = reporting_service.generate_weekly_summary()
        return jsonify({
            'success': True,
            'data': summary
        }), 200
    except Exception as e:
        return handle_error(e)

@bp.route('/send-daily-report', methods=['POST'])
def send_daily_report():
    """Send daily report to managers"""
    try:
        from flask import request
        data = request.get_json() or {}
        manager_emails = data.get('emails', [])
        
        if not manager_emails:
            return jsonify({
                'success': False,
                'message': 'Manager emails required'
            }), 400
        
        sent = reporting_service.send_daily_report_to_managers(manager_emails)
        return jsonify({
            'success': True,
            'message': 'Daily report sent',
            'sent': sent
        }), 200
    except Exception as e:
        return handle_error(e)

@bp.route('/send-weekly-summary', methods=['POST'])
def send_weekly_summary():
    """Send weekly summary to managers"""
    try:
        from flask import request
        data = request.get_json() or {}
        manager_emails = data.get('emails', [])
        
        if not manager_emails:
            return jsonify({
                'success': False,
                'message': 'Manager emails required'
            }), 400
        
        sent = reporting_service.send_weekly_summary_to_managers(manager_emails)
        return jsonify({
            'success': True,
            'message': 'Weekly summary sent',
            'sent': sent
        }), 200
    except Exception as e:
        return handle_error(e)

@bp.route('/dashboard-metrics', methods=['GET'])
def get_dashboard_metrics():
    """Get dashboard metrics"""
    try:
        metrics = performance_service.get_dashboard_metrics()
        return jsonify({
            'success': True,
            'data': metrics
        }), 200
    except Exception as e:
        return handle_error(e)

@bp.route('/trends', methods=['GET'])
def get_trends():
    """Get trend data"""
    try:
        from flask import request
        days = request.args.get('days', 30, type=int)
        trends = performance_service.get_trend_data(days)
        return jsonify({
            'success': True,
            'data': trends
        }), 200
    except Exception as e:
        return handle_error(e)

@bp.route('/performance-summary', methods=['GET'])
def get_performance_summary():
    """Get performance summary"""
    try:
        summary = performance_service.get_performance_summary()
        return jsonify({
            'success': True,
            'data': summary
        }), 200
    except Exception as e:
        return handle_error(e)

@bp.route('/backup', methods=['POST'])
def create_backup():
    """Create data backup"""
    try:
        success = backup_service.backup_all_data()
        return jsonify({
            'success': success,
            'message': 'Backup completed' if success else 'Backup failed'
        }), 200 if success else 500
    except Exception as e:
        return handle_error(e)

