#!/bin/sh
set -ux
K_NS=default
printf 'K_NS: %s' "${K_NS}"

set +eux
BIN_KUBECTL="$(which kubectl)"
[ -z "${BIN_KUBECTL}" ] && echo "ERR: NO KUBECTL FOUND" && exit 1
printf 'FOUND KUBECTL: %s\n' "${BIN_KUBECTL}"

BIN_HELM="$(which helm)"
[ -z "${BIN_HELM}" ] && echo "ERR: NO HELM FOUND" && exit 1
BIN_HELM_VER=$(helm version|awk -F'"' '{print $2}')
printf 'FOUND HELM: %s,Version: %s\n' "${BIN_HELM}" "${BIN_HELM_VER}"
EXT_PARAM="$1"
printf 'PARAMS: %s\n' "${EXT_PARAM}"
set -ux

# shellcheck disable=SC2120
deployNs(){
  set +u
  PARAM_REV="$1"
  PARAM_COMM="apply"
  [ -n "$PARAM_REV" ] && PARAM_COMM="delete"
  set -u
  "$BIN_KUBECTL" "${PARAM_COMM}" -f ./non-helm/ns.yaml
}

# shellcheck disable=SC2120
deployHelm(){
  set +u
  PARAM_CHART_NAME="$1"
  PARAM_REV="$2"
  PARAM_COMM="upgrade --install"
  [ -n "$PARAM_REV" ] && PARAM_COMM="uninstall"
  set -u
  # shellcheck disable=SC2086
  [ -z "$PARAM_REV" ] && "$BIN_HELM" -n ${PARAM_CHART_NAME} ${PARAM_COMM} ${PARAM_CHART_NAME} ./charts/${PARAM_CHART_NAME}
  [ -n "$PARAM_REV" ] && "$BIN_HELM" -n ${PARAM_CHART_NAME} ${PARAM_COMM} ${PARAM_CHART_NAME} 
}

deploy(){
  deployNs
}

case "$EXT_PARAM" in
  "deploy-ns")
    deployNs
    ;;

  "deploy-jenkins")
    deployHelm jenkins
    ;;

  "deploy-rabbitmq")
    deployHelm rabbitmq
    ;;

  "deploy")
    deploy
    ;;

  "destroy-rabbitmq")
      deployHelm rabbitmq rev
    ;;


  "destroy")
    deployNs rev
    ;;

  *)
    echo "default just bulding"
    ;;
        
esac
