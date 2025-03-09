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
  # shellcheck disable=SC2086
  [ -n "$PARAM_REV" ] && "$BIN_HELM" -n ${PARAM_CHART_NAME} ${PARAM_COMM} ${PARAM_CHART_NAME} 
}

# shellcheck disable=SC2120
deployRabbit(){
  PARAM_REV="$1"
  # shellcheck disable=SC2086
  deployHelm rabbitmq $PARAM_REV
}

# shellcheck disable=SC2120
deployJenkins(){
  PARAM_REV="$1"
  PARAM_COMMAND=apply
  [ -n "${PARAM_COMMAND}" ] && PARAM_COMMAND=delete
  # shellcheck disable=SC2086
  deployHelm jenkins $PARAM_REV
  sleep 5s
  "${BIN_KUBECTL}" -n project-cloud-arch "$PARAM_COMMAND" -f ./non-helm/jenkins-allow-deploy.yaml
}

# shellcheck disable=SC2120
deploy(){
  deployNs
  deployJenkins
  deployRabbit
}

destroy(){
  deployRabbit "${PARAM_REV}"
  deployJenkins  "${PARAM_REV}"
  deployNs "${PARAM_REV}"
}

case "$EXT_PARAM" in
  "deploy-ns")
    deployNs
    ;;

  "deploy-jenkins")
    deployJenkins
    ;;

  "deploy-rabbitmq")
    deployRabbit
    ;;

  "deploy")
    deploy
    ;;

  "destroy-jenkins")
    deployJenkins rev
    ;;

  "destroy-rabbitmq")
    deployRabbit rev
    ;;


  "destroy-ns")
    deployNs rev
    ;;


  "destroy")
    destroy
    ;;

  *)
    echo "no target given possibie targets: deploy, destroy, deploy-ns, deploy-jenkins, deploy-rabbitmq, destroy-ns, destroy-jenkins, destroy-rabbitmq"
    ;;
        
esac
